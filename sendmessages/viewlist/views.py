from django.shortcuts import render


def view_list(request):
   return render(request, 'viewlist/viewlist.html', {})
