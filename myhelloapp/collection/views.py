from django.shortcuts import render,redirect
from collection.forms import ThingForm, ContactForm, ThingUploadForm
from collection.models import Thing, Upload
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.core.mail import mail_admins
from django.contrib import messages

# Index View, show the things.
def index(request):
	# grab all the objects
	things = Thing.objects.all()
	return render(request, 'index.html', {
		'things': things,
	})
	
# Show the details of a single thing.	
def thing_detail(request, slug):
	# grab the object...
	thing = Thing.objects.get(slug=slug)
	
	# new line! grab all the object's social accounts
	social_accounts = thing.social_accounts.all()
	
	uploads = thing.uploads.all()

	# and pass to the template
	return render(request, 'things/thing_detail.html', {
		'thing': thing,
		'social_accounts': social_accounts,
		'uploads' : uploads,
	})

# Edit the thing
@login_required
def edit_thing(request, slug):
	# grab the object
	thing = Thing.objects.get(slug=slug)
	
	# make sure the logged in user is the owner of the thing
	if thing.user != request.user:
		raise Http404

	# set the form we're using
	form_class = ThingForm
		
	# if we're coming to this view from a submitted form
	if request.method == 'POST':
		# grab the data from the submitted form and apply to the form
		form = form_class(data=request.POST, instance=thing)
		if form.is_valid():
			# save the new data
			form.save()
			
			messages.success(request, 'Thing details updated.')
			
			return redirect('thing_detail', slug=thing.slug)
	# otherwise just create the form
	else:
		form = form_class(instance=thing)

	# and render the template
	return render(request, 'things/edit_thing.html', {
	'thing': thing,
	'form': form,
	})

# Create a new thing.	
def create_thing(request):
	form_class = ThingForm
	
	# if we're coming from a submitted form, do this
	if request.method == 'POST':
		# grab the data from the submitted form and
		# apply to the form
		form = form_class(request.POST)
		if form.is_valid():
			# create an instance but don’t save yet
			thing = form.save(commit=False)

			# set the additional details
			thing.user = request.user
			thing.slug = slugify(thing.name)

			# save the object
			thing.save()
			
			mail_admins("New thing created", "Un usuario creo una cosa")

			# redirect to our newly created thing
			return redirect('thing_detail', slug=thing.slug)

	# otherwise just create the form
	else:
		form = form_class()

	return render(request, 'things/create_thing.html', {
	'form': form,
	})

# Browse the things by name.
def browse_by_name(request, initial=None):
	if initial:
		things = Thing.objects.filter(name__istartswith=initial)
		things = things.order_by('name')
	else:
		things = Thing.objects.all().order_by('name')
		
	return render(request, 'search/search.html', {
		'things': things,
		'initial': initial,
		})

# Contact Form		
def contact(request):
	form_class = ContactForm

	# new logic!
	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = form.cleaned_data['contact_name']
			contact_email = form.cleaned_data['contact_email']
			form_content = form.cleaned_data['content']

			# Email the profile with the contact info
			template = get_template('contact_template.txt')

			context = Context({
			'contact_name': contact_name,
			'contact_email': contact_email,
			'form_content': form_content,
			})
			content = template.render(context)

			email = EmailMessage(
			'New contact form submission',
			content,
			'Your website <hi@weddinglovely.com>',
			['youremail@gmail.com'],
			headers = {'Reply-To': contact_email }
			)
			email.send()
			return redirect('contact')

	return render(request, 'contact.html', {
	'form': form_class,
	})
	
@login_required
def edit_thing_uploads(request, slug):
	#grab the object
	thing = Thing.objects.get(slug=slug)
	
	#double checking just for security
	if thing.user != request.user:
		raise Http404
		
	#set the form we are using
	form_class = ThingUploadForm
	
	#if we're commingto this view from a submitted form
	if request.method == 'POST':
		#grab the data from the submitted form
		#note the new "file" part
		form = form_class(data=request.POST,
			files=request.FILES, instance=thing)
		if form.is_valid():
			
			#create a new object from the submited form
			Upload.objects.create(
				image=form.cleaned_data['image'],
				thing=thing,
				)
			return redirect('edit_thing_uploads', slug=thing.slug)
		
	#otherwise just create the form
	else:
		form = form_class(instance=thing)
	
	#grab all the object's images
	uploads = thing.uploads.all()
	
	#and render the templates
	return render(request, 'things/edit_thing_uploads.html', {
		'thing' : thing,
		'form' : form,
		'uploads' : uploads,
	})

@login_required
def delete_upload(request, id):
	#grab the image
	upload = Upload.objects.get(id=id)
	
	#security check
	if upload.thing.user != request.user:
		raise Http404
	
	#delete the image
	upload.delete()
	
	#refresh the edit page
	return redirect('edit_thing_uploads', slug=upload.thing.slug)