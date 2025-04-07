from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import AdForm
from .models import house
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('home')  # Redirect to home page
    else:
         form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def home(request):
    return render(request, 'accounts/index.html')  # Render the home page template


@login_required
def buy(request):
    # Fetch unique property types and locations for filters
    property_types = house.objects.values_list('property_type', flat=True).distinct()
    locations = [f'D{i}' for i in range(1, 25)]

    # Get all houses to start with
    houses = house.objects.all()

    # Get filter and search parameters from the request
    search_query = request.GET.get('search', '')
    selected_property_type = request.GET.get('property_type', '')
    selected_location = request.GET.get('location', '')
    max_price = request.GET.get('price', '').strip()
    beds = request.GET.get('beds', '').strip()
    baths = request.GET.get('baths', '').strip()

    price_range = range(500, 5500, 500)
    bed_range = range(1, 9)
    bath_range = range(1, 9)

    # Featured properties (optional logic to customize later)
    featured_properties = house.objects.order_by('-date_posted')[:5]

    print(f"Filters received - price: {max_price}, beds: {beds}, baths: {baths}")

    # Apply search filter
    if search_query:
        houses = houses.filter(
            Q(description__icontains=search_query) | Q(location__icontains=search_query)
        )

    # Apply property type filter
    if selected_property_type:
        houses = houses.filter(property_type=selected_property_type)

    # Apply location filter
    if selected_location:
        if selected_location.startswith("D") and selected_location[1:].isdigit():
            district_number = selected_location[1:]
            if len(district_number) == 1:
                houses = houses.filter(location__startswith=f"D0{district_number}")
            else:
                houses = houses.filter(location__startswith=selected_location)
        else:
            houses = houses.filter(location__startswith=selected_location)

    # Apply price filter
    try:
        max_price_int = int(max_price)
        houses = houses.filter(rent__lte=max_price_int)
    except (ValueError, TypeError):
        max_price_int = ''

    # Apply bed filter
    try:
        beds_int = int(beds)
        houses = houses.filter(number_of_bedrooms=beds_int)
    except (ValueError, TypeError):
        beds_int = ''

    # Apply bath filter
    try:
        baths_int = int(baths)
        houses = houses.filter(number_of_bathrooms=baths_int)
    except (ValueError, TypeError):
        baths_int = ''

    # Send everything to the template
    context = {
        'app_name': 'Rental Dublin',
        'property_types': property_types,
        'locations': locations,
        'results': houses,
        'featured_properties': featured_properties,
        'search_query': search_query,
        'selected_property_type': selected_property_type,
        'selected_location': selected_location,
        'price': max_price_int,
        'beds': beds_int,
        'baths': baths_int,
        'price_range': price_range,
        'bed_range': bed_range,
        'bath_range': bath_range,
    }

    return render(request, 'accounts/buy.html', context)


@login_required
def item_details(request, property_id):
    # Fetch item details from the database
    Item = get_object_or_404(house, property_id=property_id)

    # Context data for the details page
    context = {
        'app_name': 'Rental Dublin',
        'house': Item,
    }
    return render(request, 'accounts/item_details.html', context)



@login_required
def post_ad(request):
    if request.method == 'POST':
        print("POST request received")
        # Bind the form to the POST data and files
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            ad = form.save(commit=False)
            # Assign the logged-in user as the seller
            ad.seller = request.user
            form.save()
            # Redirect to a success page or the homepage
            return redirect('buy')  # Replace 'dashboard' with your success URL name
        else:
            # If the form is invalid, re-render the form with errors
            print("Form errors:", form.errors)  # Debugging: Print form errors
    else:
        print("GET request received")
        # If it's a GET request, create a new empty form
        form = AdForm()
    # Render the post_ad template with the form
    return render(request, 'accounts/post_ad.html', {'form': form})

@login_required
def update_details(request,property_id):
    ad1 = house.objects.get(property_id=property_id)
    if request.method == 'POST':
        form = AdForm(request.POST,request.FILES, instance = ad1)
        if form.is_valid():
            form.save()
            return redirect('buy')
    else :
        form = AdForm(instance=ad1)
        return render(request, 'accounts/update_ad.html', {'form': form})
    
@login_required
def delete_ad(request, property_id):
    ad1 = get_object_or_404(house, property_id=property_id)
    ad1.delete()
    return redirect('My_ads')    

@login_required
def My_ads(request):
    # Fetch item details from the database
    update_item = house.objects.filter(seller_id = request.user)
    # update_item = item.objects.all()
    # Context data for the details page
    context = { 
        'items' : update_item
    }
    return render(request, 'accounts/update.html', context)
    