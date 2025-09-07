from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from .models import Message, PDFFile, Doubt
from django.shortcuts import redirect
from .forms import MessageForm, PDFUploadForm, DoubtForm
from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'core/group_list.html', {'groups': groups})

# def group_detail(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     messages = Message.objects.filter(group=group).order_by('timestamp')
#     pdfs = PDFFile.objects.filter(group=group)
#     doubts = Doubt.objects.filter(group=group)

#     if request.method == 'POST':
#         if 'send_message' in request.POST:
#             message_form = MessageForm(request.POST)
#             if message_form.is_valid():
#                 msg = message_form.save(commit=False)
#                 msg.group = group
#                 msg.sender = request.user
#                 msg.save()
#                 return redirect('group_detail', group_id=group.id)
#         elif 'upload_pdf' in request.POST:
#             pdf_form = PDFUploadForm(request.POST, request.FILES)
#             if pdf_form.is_valid():
#                 pdf = pdf_form.save(commit=False)
#                 pdf.group = group
#                 pdf.uploaded_by = request.user
#                 pdf.save()
#                 return redirect('group_detail', group_id=group.id)
#         elif 'submit_doubt' in request.POST:
#             doubt_form = DoubtForm(request.POST)
#             if doubt_form.is_valid():
#                 doubt = doubt_form.save(commit=False)
#                 doubt.group = group
#                 doubt.asked_by = request.user
#                 doubt.save()
#                 return redirect('group_detail', group_id=group.id)
#     else:
#         message_form = MessageForm()
#         pdf_form = PDFUploadForm()
#         doubt_form = DoubtForm()

#     return render(request, 'core/group_detail.html', {
#         'group': group,
#         'messages': messages,
#         'pdfs': pdfs,
#         'doubts': doubts,
#         'message_form': message_form,
#         'pdf_form': pdf_form,
#         'doubt_form': doubt_form,
#     })
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = Message.objects.filter(group=group).order_by('timestamp')
    pdfs = PDFFile.objects.filter(group=group)
    doubts = Doubt.objects.filter(group=group)

    if request.method == 'POST':
        if 'send_message' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                msg = message_form.save(commit=False)
                msg.group = group
                msg.sender = request.user
                msg.save()
                return redirect('group_detail', group_id=group_id)

        elif 'upload_pdf' in request.POST:
            hashtag = request.POST.get('pdf_hashtag', '').strip()
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file and hashtag:
                pdf = PDFFile.objects.create(
                    group=group,
                    uploaded_by=request.user,
                    file=pdf_file,
                    hashtag=hashtag
                )
                return redirect('group_detail', group_id=group_id)

        elif 'submit_doubt' in request.POST:
            hashtag = request.POST.get('doubt_hashtag', '').strip()
            question = request.POST.get('doubt_content', '').strip()
            if question and hashtag:
                Doubt.objects.create(
                    group=group,
                    asked_by=request.user,
                    question=question,
                    hashtag=hashtag,
                    is_resolved=False
                )
                return redirect('group_detail', group_id=group_id)

    context = {
        'group': group,
        'messages': messages,
        'pdfs': pdfs,
        'doubts': doubts,
        'message_form': MessageForm(),
        # Other forms as needed
    }
    return render(request, 'core/group_detail.html', context)



def resolve_doubt(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)
    # Only allow teachers (staff) to resolve doubts
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to resolve doubts.")
    doubt.is_resolved = True
    doubt.save()
    return redirect('group_detail', group_id=doubt.group.id)


@login_required
def user_type_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            success = True  # indicate success to template
            form = UserProfileForm()  # reset form blank for another entry
        else:
            success = False
    else:
        form = UserProfileForm()
        success = False
        
    return render(request, 'user_type.html', {'form': form, 'success': success})
