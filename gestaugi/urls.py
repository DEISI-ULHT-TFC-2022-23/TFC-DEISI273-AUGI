from django.shortcuts import render
from . import views
from django.urls import path, include

app_name = "gestaugi"

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('partners/', views.partners_page_view, name='partners'),
    path('newpartner/', views.newpartner, name='newpartner'),
    path('viewpartner/<int:socio_id>', views.viewpartner, name="viewpartner"),
    path('editpartner/<int:socio_id>',views.editpartner,name="editpartner"),
    path('deletepartner/<int:socio_id>', views.deletepartner, name='deletepartner'),
    path('lots/', views.lots_page_view, name='lots'),
    path('newlot/', views.newlot, name='newlot'),
    path('viewlot/<int:lote_id>', views.viewlot, name="viewlot"),
    path('editlot/<int:lote_id>', views.editlot, name="editlot"),
    path('deletelot/<int:lote_id>', views.deletelot, name='deletelot'),
    path('coparticipation/', views.coparticipation_page_view, name='coparticipation'),
    path('newcoparticipation/', views.newcoparticipation, name='newcoparticipation'),
    path('viewcoparticipation/<int:compart_id>', views.viewcoparticipation, name='viewcoparticipation'),
    path('editcoparticipation/<int:compart_id>', views.editcoparticipation, name='editcoparticipation'),
    path('deletecoparticipation/<int:compart_id>', views.deletecoparticipation, name='deletecoparticipation'),
    path('load_lots/', views.load_lots, name='load_lots'),
    path('assembly/', views.assembly_page_view, name='assembly'),
    path('newassembly/', views.newassembly, name='newassembly'),
    path('viewassembly/<int:assembleia_id>', views.viewassembly, name="viewassembly"),
    path('editassembly/<int:assembleia_id>', views.editassembly, name="editassembly"),
    path('deleteassembly/<int:assembleia_id>', views.deleteassembly, name='deleteassembly'),
    path('attendance/', views.attendance_page_view, name='attendance'),
    path('newattendance/', views.newattendance, name='newattendance'),
    path('viewattendance/<int:presenca_id>', views.viewattendance, name='viewattendance'),
    path('editattendance/<int:presenca_id>', views.editattendance, name='editattendance'),
    path('deleteattendance/<int:presenca_id>', views.deleteattendance, name='deleteattendance'),
    path('load_dates/', views.load_dates, name='load_dates'),
    path('load_dates4edit/<int:presenca_id>', views.load_dates4edit, name='load_dates4edit'),
    path('expenses/', views.expenses_page_view, name='expenses'),
    path('newexpense/', views.newexpense, name='newexpense'),
    path('viewexpense/<int:despesa_id>', views.viewexpense, name="viewexpense"),
    path('editexpense/<int:despesa_id>', views.editexpense, name="editexpense"),
    path('deletexpense/<int:despesa_id>', views.deletexpense, name="deletexpense"),
    path('annuities/', views.annuities_page_view, name='annuities'),
    path('newannuity/', views.newannuity, name='newannuity'),
    path('viewannuity/<int:anuidade_id>', views.viewannuity, name='viewannuity'),
    path('editannuity/<int:anuidade_id>', views.editannuity, name="editannuity"),
    path('deleteannuity/<int:anuidade_id>', views.deleteannuity, name='deleteannuity'),
    path('payments/', views.payments_page_view, name='payments'),
    path('newpayment/', views.newpayment, name='newpayment'),
    path('viewpayment/<int:pagamento_id>', views.viewpayment, name="viewpayment"),
    path('editpayment/<int:pagamento_id>', views.editpayment, name="editpayment"),
    path('deletepayment/<int:pagamento_id>', views.deletepayment, name="deletepayment"),
    path("reports/", views.reports, name="reports"),
    path("listpartners2pdf/", views.listpartners2pdf, name="listpartners2pdf"),
    path("listpartners2csv/", views.listpartners2csv, name="listpartners2csv"),
    path("listdebts2pdf/", views.listdebts2pdf, name="listdebts2pdf"),
    path("listdebts2csv/", views.listdebts2csv, name="listdebts2csv"),
    path("listcomparts2pdf/", views.listcomparts2pdf, name="listcomparts2pdf"),
    path("listcomparts2csv/", views.listcomparts2csv, name="listcomparts2csv"),
    path("listpayments2pdf/", views.listpayments2pdf, name="listpayments2pdf"),
    path("listpayments2csv/", views.listpayments2csv, name="listpayments2csv"),
    path("listtotpayments2pdf/", views.listtotpayments2pdf, name="listtotpayments2pdf"),
    path("listtotpayments2csv/", views.listtotpayments2csv, name="listtotpayments2csv"),
    path("listexpenses2pdf/", views.listexpenses2pdf, name="listexpenses2pdf"),
    path("listexpenses2csv/", views.listexpenses2csv, name="listexpenses2csv"),
    path("listotexpenses2pdf/", views.listotexpenses2pdf, name="listotexpenses2pdf"),
    path("listotexpenses2csv/", views.listotexpenses2csv, name="listotexpenses2csv"),
    path("settings/", views.settings, name="settings"),
    path("expensestypes/", views.expensestypes_page_view, name="expensestypes"),
    path('newexpensetype/', views.newexpensetype, name='newexpensetype'),
    path('viewexpensetype/<int:tipo_id>', views.viewexpensetype, name="viewexpensetype"),
    path('editexpensetype/<int:tipo_id>', views.editexpensetype, name="editexpensetype"),
    path('deletexpensetype/<int:tipo_id>', views.deletexpensetype, name="deletexpensetype"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expensesbytype/', views.expensesbytype, name='expensesbytype'),
    path('dispmessage/', views.dispmessage, name='dispmessage'),
    path("parameters/", views.parameters_page_view, name="parameters"),
    path("divdashboard/", views.divdashboard_page_view, name="divdashboard"),
    path('infodashboard/', views.infodashboard, name='infodashboard'),
    path("divdashboard2/", views.divdashboard2_page_view, name="divdashboard2"),
    path('infodashboard2/', views.infodashboard2, name='infodashboard2'),
    path("divdashboard3/", views.divdashboard3_page_view, name="divdashboard3"),
    path('infodashboar3/', views.infodashboard3, name='infodashboard3'),
    path("divdashboard4/", views.divdashboard4_page_view, name="divdashboard4"),
    path('infodashboar4/', views.infodashboard4, name='infodashboard4'),
    path("divdashboard5/", views.divdashboard5_page_view, name="divdashboard5"),
    path('infodashboar5/', views.infodashboard5, name='infodashboard5'),
]
