from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """ Allow signups via Web3 without email """
        return True
    
    def save_user(self, request, user, form, commit=True):
        """ Custom user save for Web3 addresses """
        if hasattr(form, 'cleaned_data') and 'address' in form.cleaned_data:
            user.username = form.cleaned_data['address'].lower()
        return super().save_user(request, user, form, commit)