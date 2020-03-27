from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .models import Collection, Picture, Document
from .forms import PictureUploadForm
from .filters import DocumentFilter
from .tables import DocumentTable

import os


def picture_index(request):
    collections = Collection.objects.filter(type="Pictures").order_by('-pub_date')
    context = {
        'type': "pictures",
        'collections': collections,
    }
    return render(request, 'archive/index.html', context)


class FilteredDocumentsListView(SingleTableMixin, FilterView):
    model = Document
    paginate_by = 15
    table_class = DocumentTable
    template_name = 'archive/document_index.html'
    filterset_class = DocumentFilter


class DetailView(generic.DetailView):
    model = Collection
    template_name = 'archive/detail.html'


def edit(request, pk):
    collection = Collection.objects.get(id=pk)
    return render(request, 'archive/edit.html', {'collection': collection})


def remove_file(request, collection_id, file_id):
    file = Picture.objects.get(pk=file_id)
    file.delete()
    collection = Collection.objects.get(pk=collection_id)
    if collection.picture_set.count() > 0:
        return render(request, 'archive/edit.html', {'collection': collection})
    collection.delete()
    collections = Collection.objects.all()
    return render(request, 'archive/index.html', {'collections': collections})


def upload(request):
    if request.method == 'POST':
        form = PictureUploadForm(request.POST)
        if form.is_valid():
            if request.FILES.getlist('images') is None:
                return redirect('archive:pictures')
            collection = Collection(title=form['album'].value(), type='Pictures')
            collection.save()
            for file in request.FILES.getlist('images'):
                Picture(image=file, collection=collection).save()
        return redirect('archive:pictures')

    form = PictureUploadForm
    context = {
        'picture_form': form,
    }
    return render(request, 'archive/upload.html', context)


def clean_media(request):
    folders = os.walk(settings.MEDIA_ROOT)
    for f in folders:
        print(f[0])
        print(f[2])
        # If picture not in any collection, remove it.
    return redirect('archive:pictures')
