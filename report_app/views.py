from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages


# Generate PDF report
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from order_app.models import *


def report_generator(request, orders):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4, bottomup=0)
    c.setAuthor("Deskly")
    c.setTitle("Deskly order report")

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    max_orders_per_page = 4
    max_lines_per_page = 40
    order_count = 0
    line_count = 0
    entry_count = 0
    lines = []

    order_count = orders.count()
    page_count = (order_count + max_orders_per_page - 1) // max_orders_per_page

    for page in range(page_count):
        lines.clear()

        start_index = page * max_orders_per_page
        end_index = start_index + max_orders_per_page
        page_orders = orders[start_index:end_index]

        for order in page_orders:
            lines.append("===========================Start===========================")
            lines.append("Order ID:" + str(order.id))
            lines.append("Order ID:" + str(order.payment))
            lines.append("Date:" + str(order.date))
            lines.append("Status:" + str(order.status))
            lines.append("Address-name:" + str(order.address.name))
            lines.append("Address-email:" + str(order.address.email))
            lines.append("Address-line-1:" + str(order.address.line_1))
            lines.append("Payment:" + str(order.net_total))
            lines.append("===========================End===========================")

        for line in lines:
            line_count += 1
            textob.textLine(line)
            if line_count % max_lines_per_page == 0:
                c.drawText(textob)
                c.showPage()
                textob = c.beginText()
                textob.setTextOrigin(inch, inch)
                textob.setFont("Helvetica", 14)
    c.save()
    buf.seek(0)
    request.session["messages"] = "Report successfully generated"
    return FileResponse(buf, as_attachment=True, filename="test_report_june.pdf")


def report_pdf_order(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        if not from_date or not to_date:
            return HttpResponse("Please provide both from_date and to_date.")
        try:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Invalid date format.")
        orders = Order.objects.filter(date__date__range=[from_date, to_date]).order_by(
            "-id"
        )
        print(orders)
        messages.success(request, "Report successfully generated")
        return report_generator(request, orders)

    if "messages" in request.session:
        messages.success(request, request.session.pop("messages"))
    context = {}
    return render(request, "report_pdf_order.html", context)


def chart_demo(request):
    orders = Order.objects.order_by("-id")[:5]
    labels = []
    data = []
    for order in orders:
        labels.append(order.id)
        data.append(order.net_total)
    context = {
        "labels": labels,
        "data": data,
    }

    return render(request, "chart_demo.html", context)


# Chart_customer_dashboard_order
def chart_customer_dashboard_order(request):
    orders = Order.objects.filter(customer=request.user).order_by("-id")[:5]
    labels = []
    data = []
    for order in orders:
        labels.append(order.id)
        data.append(order.net_total)
    context = {
        "labels": labels,
        "data": data,
    }

    return render(request, "chart_customer_dashboard_order.html", context)


# Sample methods
def example_form(request):
    context = {}
    return render(request, "example_form.html", context)
