from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from .forms import NewItemForm, EditItemForm
from .models import item, Category

import os

def browse(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    items = item.objects.filter(is_sold=False)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        items = items.filter(category_id=category_id)

    return render(request, 'item/browse.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def search_documents(request):
    query = request.GET.get("query", "")
    reverse_order = request.GET.get("reverse", "false")
    index_path = os.path.join(settings.BASE_DIR, "indexdir")
    results = []
    if query:
        ix = open_dir(index_path)
        with ix.searcher() as searcher:
            query_obj = QueryParser("content", ix.schema).parse(query)
            results = searcher.search(query_obj, limit=10, sortedby="content")

            results = [{
                    "path": os.path.join(settings.MEDIA_URL, res["path"].lstrip("./").lstrip("media/")).replace("\\", "/"),
                    "title": res["title"]
                } for res in results]
            
            if reverse_order.lower() == "true":
                results.reverse()
            return render(request, "item/search_documents.html", {
                    "results": results,
                    "query": query,
                    "reverse_order": "false" if reverse_order == "true" else "true"
                }
            )


def predictive_search(request):
    query = request.GET.get('query', '').strip()

    suggestions = []

    if query:
        items = item.objects.filter((Q(name__icontains=query)))[:5]
        suggestions = [{"id": Item.id, "name": Item.name, "image": Item.image.url, "price": float(Item.price)} for Item in items]

    return JsonResponse(suggestions, safe=False)

def detail(request, pk):
    item_input = get_object_or_404(item, pk=pk)

    related_items = item.objects.filter(category=item_input.category, is_sold=False).exclude(pk=pk)[0:3]


    return render(request, 'item/detail.html', {
        'item': item_input,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
        
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item'
    })

@login_required
def edit(request, pk):
    return_item = get_object_or_404(item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=return_item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=return_item.id)
        
    else:
        form = EditItemForm(instance=return_item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item'
    })

@login_required
def delete(request, pk):
    return_item = get_object_or_404(item, pk=pk, created_by=request.user)
    return_item.delete()

    return redirect('dashboard:index')