import json
import urllib.parse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from .models import (
    Cpu,
    Motherboard,
    Memory,
    Case,
    CpuCooler,
    InternalHardDrive,
    Os,
    VideoCard,
    PowerSupply,
)
from .compatibility import (
    filter_compatible_motherboards,
    filter_compatible_cases_by_motherboard,
    filter_compatible_psu,
)
from accounts.models import SavedBuild


def index(request):
    compatibility_on = request.session.get("compatibility_on", True)
    return render(request, "main/index.html", {"compatibility_on": compatibility_on})


def toggle_compatibility(request):
    current = request.session.get("compatibility_on", True)
    request.session["compatibility_on"] = not current
    return redirect("main:index")


def list_components(request, category):
    compatibility_on = request.session.get("compatibility_on", True)

    selected_cpu_id = request.session.get("build_cpu")
    selected_motherboard_id = request.session.get("build_motherboard")
    selected_os_id = request.session.get("build_os")

    current_cpu = Cpu.objects.filter(id=selected_cpu_id).first() if selected_cpu_id else None
    current_motherboard = Motherboard.objects.filter(id=selected_motherboard_id).first() if selected_motherboard_id else None
    current_os = Os.objects.filter(id=selected_os_id).first() if selected_os_id else None

    model_map = {
        "cpu": Cpu,
        "motherboard": Motherboard,
        "memory": Memory,
        "case": Case,
        "cpu_cooler": CpuCooler,
        "hdd": InternalHardDrive,
        "os": Os,
        "video_card": VideoCard,
        "powersupply": PowerSupply,
    }
    model_class = model_map.get(category)
    if not model_class:
        return HttpResponseBadRequest("Некорректная категория")

    items = model_class.objects.all()

    if compatibility_on:
        if category == "motherboard" and current_cpu:
            items = filter_compatible_motherboards(current_cpu, items)
        elif category == "case" and current_motherboard:
            items = filter_compatible_cases_by_motherboard(current_motherboard, items)
        elif category == "powersupply":
            items = filter_compatible_psu(
                items,
                cpu=current_cpu,
                gpu=VideoCard.objects.filter(id=request.session.get("build_video_card")).first(),
                memory=Memory.objects.filter(id=request.session.get("build_memory")).first(),
                hdd=InternalHardDrive.objects.filter(id=request.session.get("build_hdd")).first(),
            )

    context = {
        "category": category,
        "items": items,
        "compatibility_on": compatibility_on,
    }
    return render(request, "main/category_list.html", context)


@login_required
def add_to_build(request, category, item_id):
    build_map = {
        "cpu": "build_cpu",
        "motherboard": "build_motherboard",
        "memory": "build_memory",
        "case": "build_case",
        "cpu_cooler": "build_cpu_cooler",
        "hdd": "build_hdd",
        "os": "build_os",
        "video_card": "build_video_card",
        "powersupply": "build_powersupply"
    }
    key = build_map.get(category)
    if not key:
        return HttpResponseBadRequest("Некорректная категория")

    model_map = {
        "cpu": Cpu,
        "motherboard": Motherboard,
        "memory": Memory,
        "case": Case,
        "cpu_cooler": CpuCooler,
        "hdd": InternalHardDrive,
        "os": Os,
        "video_card": VideoCard,
        "powersupply": PowerSupply,
    }
    model_class = model_map.get(category)
    try:
        model_class.objects.get(id=item_id)
    except model_class.DoesNotExist:
        return HttpResponseBadRequest("Такого объекта не существует")

    request.session[key] = item_id
    request.session.modified = True
    return redirect("main:show_build")


@login_required
def show_build(request):
    build_cpu_id = request.session.get("build_cpu")
    build_motherboard_id = request.session.get("build_motherboard")
    build_memory_id = request.session.get("build_memory")
    build_case_id = request.session.get("build_case")
    build_cpu_cooler_id = request.session.get("build_cpu_cooler")
    build_hdd_id = request.session.get("build_hdd")
    build_os_id = request.session.get("build_os")
    build_video_card_id = request.session.get("build_video_card")
    build_powersupply_id = request.session.get("build_powersupply")

    selected_cpu = Cpu.objects.filter(id=build_cpu_id).first() if build_cpu_id else None
    selected_motherboard = Motherboard.objects.filter(id=build_motherboard_id).first() if build_motherboard_id else None
    selected_memory = Memory.objects.filter(id=build_memory_id).first() if build_memory_id else None
    selected_case = Case.objects.filter(id=build_case_id).first() if build_case_id else None
    selected_cpu_cooler = CpuCooler.objects.filter(id=build_cpu_cooler_id).first() if build_cpu_cooler_id else None
    selected_hdd = InternalHardDrive.objects.filter(id=build_hdd_id).first() if build_hdd_id else None
    selected_os = Os.objects.filter(id=build_os_id).first() if build_os_id else None
    selected_video_card = VideoCard.objects.filter(id=build_video_card_id).first() if build_video_card_id else None
    sellected_powersupply = PowerSupply.objects.filter(id=build_powersupply_id).first() if build_powersupply_id else None

    context = {
        "cpu": selected_cpu,
        "motherboard": selected_motherboard,
        "memory": selected_memory,
        "case": selected_case,
        "cpu_cooler": selected_cpu_cooler,
        "hdd": selected_hdd,
        "os": selected_os,
        "video_card": selected_video_card,
        "powersupply": sellected_powersupply,
    }
    return render(request, "main/build.html", context)


def remove_from_build(request, category):
    build_map = {
        "cpu": "build_cpu",
        "motherboard": "build_motherboard",
        "memory": "build_memory",
        "case": "build_case",
        "cpu_cooler": "build_cpu_cooler",
        "hdd": "build_hdd",
        "os": "build_os",
        "video_card": "build_video_card",
        "powersupply": "build_powersupply",
    }
    key = build_map.get(category)
    if not key:
        return HttpResponseBadRequest("Некорректная категория")

    if key in request.session:
        del request.session[key]
        request.session.modified = True
    return redirect("main:show_build")


def component_detail(request, category, item_id):
    model_map = {
        "cpu": Cpu,
        "motherboard": Motherboard,
        "memory": Memory,
        "case": Case,
        "cpu_cooler": CpuCooler,
        "hdd": InternalHardDrive,
        "os": Os,
        "video_card": VideoCard,
        "powersupply": PowerSupply,
    }
    model_class = model_map.get(category)
    if not model_class:
        return HttpResponseBadRequest("Некорректная категория")

    obj = model_class.objects.filter(id=item_id).first()
    if not obj:
        return HttpResponseBadRequest("Объект не найден")

    base_dns_url = "https://www.dns-shop.ru/search/"
    base_yandex_url = "https://market.yandex.ru/search?text="
    product_name = obj.name.strip() if obj.name else ""
    search_query = urllib.parse.quote(product_name)
    dns_link = f"{base_dns_url}?q={search_query}"
    yandex_link = f"{base_yandex_url}{search_query}"
    context = {
        "obj": obj,
        "category": category,
        "dns_link": dns_link,
        "yandex_link": yandex_link,
    }
    return render(request, "main/detail.html", context)


BUILD_MAP = {
    "build_cpu": (Cpu, "cpu"),
    "build_motherboard": (Motherboard, "motherboard"),
    "build_memory": (Memory, "memory"),
    "build_case": (Case, "case"),
    "build_cpu_cooler": (CpuCooler, "cpu_cooler"),
    "build_hdd": (InternalHardDrive, "hdd"),
    "build_os": (Os, "os"),
    "build_video_card": (VideoCard, "video_card"),
    "build_powersupply": (PowerSupply, "powersupply"),
}


@login_required
def export_build(request):
    build_data = {}

    for session_key, (ModelClass, cat_name) in BUILD_MAP.items():
        item_id = request.session.get(session_key)
        if item_id:
            obj = ModelClass.objects.filter(id=item_id).first()
            if obj:
                build_data[cat_name] = {
                    "id": obj.id,
                    "name": obj.name,
                }

    json_data = json.dumps(build_data, ensure_ascii=False, indent=2)

    response = HttpResponse(json_data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="my_build.pcbuild"'
    return response


@login_required
def import_build(request):
    if request.method == "POST":
        build_file = request.FILES.get("build_file")
        if not build_file:
            return HttpResponseBadRequest("Файл не загружен.")

        if not build_file.name.endswith(".pcbuild"):
            return HttpResponseBadRequest(
                "Неверное расширение файла. Требуется .pcbuild"
            )

        try:
            file_data = build_file.read().decode("utf-8")
            data = json.loads(file_data)
        except Exception as e:
            return HttpResponseBadRequest(f"Ошибка чтения/парсинга файла: {e}")

        for cat_name, obj_info in data.items():
            session_key_to_set = None
            model_class = None

            for session_key, (ModelClass, map_cat) in BUILD_MAP.items():
                if map_cat == cat_name:
                    session_key_to_set = session_key
                    model_class = ModelClass
                    break

            if session_key_to_set and model_class:
                item_id = obj_info.get("id")
                if item_id:
                    exists = model_class.objects.filter(id=item_id).exists()
                    if exists:
                        request.session[session_key_to_set] = item_id

        request.session.modified = True
        return redirect("main:show_build")
    else:
        return redirect("main:show_build")


@login_required
def ajax_search(request, category):
    compatibility_on = request.session.get("compatibility_on", True)
    query = request.GET.get("q", "").strip().lower()

    selected_cpu_id = request.session.get("build_cpu")
    selected_motherboard_id = request.session.get("build_motherboard")

    current_cpu = Cpu.objects.filter(id=selected_cpu_id).first() if selected_cpu_id else None
    current_motherboard = Motherboard.objects.filter(id=selected_motherboard_id).first() if selected_motherboard_id else None

    model_map = {
        "cpu": Cpu,
        "motherboard": Motherboard,
        "memory": Memory,
        "case": Case,
        "cpu_cooler": CpuCooler,
        "hdd": InternalHardDrive,
        "os": Os,
        "video_card": VideoCard,
        "powersupply": PowerSupply,
    }
    model_class = model_map.get(category)
    if not model_class:
        return JsonResponse({"error": "Некорректная категория"}, status=400)

    items = model_class.objects.all()
    if query:
        items = items.filter(name__icontains=query)

    if compatibility_on:
        if category == "motherboard" and current_cpu:
            items = filter_compatible_motherboards(current_cpu, items)
        elif category == "case" and current_motherboard:
            items = filter_compatible_cases_by_motherboard(current_motherboard, items)
        elif category == "powersupply":
            items = filter_compatible_psu(
                items,
                cpu=current_cpu,
                gpu=VideoCard.objects.filter(id=request.session.get("build_video_card")).first(),
                memory=Memory.objects.filter(id=request.session.get("build_memory")).first(),
                hdd=InternalHardDrive.objects.filter(id=request.session.get("build_hdd")).first(),
            )

    results = []
    for item in items:
        results.append({
            "id": item.id,
            "name": item.name,
            "detail_url": request.build_absolute_uri(
                reverse("main:component_detail", args=[category, item.id])
            ),
            "add_url": request.build_absolute_uri(
                reverse("main:add_to_build", args=[category, item.id])
            ),
        })

    return JsonResponse({"items": results}, safe=False)



@login_required
def save_build_to_db(request):
    from accounts.models import SavedBuild

    build_cpu_id = request.session.get("build_cpu")
    build_motherboard_id = request.session.get("build_motherboard")
    build_memory_id = request.session.get("build_memory")
    build_case_id = request.session.get("build_case")
    build_cpu_cooler_id = request.session.get("build_cpu_cooler")
    build_hdd_id = request.session.get("build_hdd")
    build_os_id = request.session.get("build_os")
    build_video_card_id = request.session.get("build_video_card")
    build_powersupply_id = request.session.get("build_powersupply")

    cpu_obj = Cpu.objects.filter(id=build_cpu_id).first() if build_cpu_id else None
    mb_obj = Motherboard.objects.filter(id=build_motherboard_id).first() if build_motherboard_id else None
    mem_obj = Memory.objects.filter(id=build_memory_id).first() if build_memory_id else None
    case_obj = Case.objects.filter(id=build_case_id).first() if build_case_id else None
    cooler_obj = CpuCooler.objects.filter(id=build_cpu_cooler_id).first() if build_cpu_cooler_id else None
    hdd_obj = InternalHardDrive.objects.filter(id=build_hdd_id).first() if build_hdd_id else None
    os_obj = Os.objects.filter(id=build_os_id).first() if build_os_id else None
    vc_obj = VideoCard.objects.filter(id=build_video_card_id).first() if build_video_card_id else None
    ps_obj = PowerSupply.objects.filter(id=build_powersupply_id).first() if build_powersupply_id else None

    build_name = "Моя сборка"

    SavedBuild.objects.create(
        user=request.user,
        build_name=build_name,
        cpu=cpu_obj,
        motherboard=mb_obj,
        memory=mem_obj,
        case=case_obj,
        cpu_cooler=cooler_obj,
        hdd=hdd_obj,
        os=os_obj,
        video_card=vc_obj,
        powersupply=ps_obj
    )
    return redirect("main:my_builds")


@login_required
def my_builds(request):
    from accounts.models import SavedBuild

    builds = SavedBuild.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "main/my_builds.html", {"builds": builds})


@login_required
def delete_build(request, build_id):
    from accounts.models import SavedBuild

    build = get_object_or_404(SavedBuild, id=build_id)
    if build.user != request.user:
        return HttpResponseBadRequest("Вы не можете удалять чужие сборки.")

    build.delete()
    return redirect("main:my_builds")
