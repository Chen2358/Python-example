class Signup(UserCreationForm):
	username = forms.CharField(min_length=4, max_length=30,
							   error_messages={
							   		'min_length': 'yonghuming buneng shaoyu 4ge zifu',
							   		'max_length': 'yonghuming buneng duoyu   30ge zifu',
							   		'required': 'yonghuming buneng weikong',
							   },
							   widget = forms.TextInput(attrs={'placeholder': 'qingshuru yonghuming'}))
	password1 = forms.CharField(min_length=8, max_length=30,
							    error_messages={
							    	'min_length': 'mima buneng shaoyu 4ge zifu',
							   		'max_length': 'mima buneng duoyu   30ge zifu',
							   		'required': 'mima buneng weikong',
							    }
							    widget=form.PasswordInput(attrs={'placeholder': 'qingshuru mima'}))
	password2 = forms.CharField(min_length=8, max_length=30,
							    error_messages={
							    	'min_length': 'mima buneng shaoyu 4ge zifu',
							   		'max_length': 'mima buneng duoyu   30ge zifu',
							   		'required': 'mima buneng weikong',
							    }
							    widget=form.PasswordInput(attrs={'placeholder': 'qingqueren mima'}))

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')