from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Comment, RatinStar, UserProfile
# from .models import Book, Comment, RatinStar, UserProfile
import datetime
from taggit.forms import TagField

# Formulário de criação de novo usuario
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sobrenome'}))
    user_image = forms.ImageField(required=False, widget = forms.widgets.FileInput(attrs={"class":"form-control"}), label = "Imagem de Perfil ( Opcional ):")
    cpf = forms.CharField(required=True, min_length=11, max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CPF (Digite Apenas Números)'}),label = "")
    bio = forms.CharField(required=False, max_length=500, widget=forms.widgets.Textarea(attrs={"placeholder":"Bio ( Opcional )", "class":"form-control"}), label="")
    state = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),label = "")
    city = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cidade'}),label = "")
    district = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bairro'}),label = "")
    house_number = forms.IntegerField(required=True,min_value=0, max_value=99999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Numero da Casa'}),label = "")
    street = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua'}),label = "")
    cep = forms.IntegerField(required=True,min_value=0, max_value=99999999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cep'}),label = "")

    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')        
        if not cpf.isdigit():
            raise ValidationError("CPF deve conter apenas números")
        if len(cpf) != 11:
            raise ValidationError("CPF deve conter 11 dígitos")                
        return cpf
    
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'cpf','email','password1','password2','bio','state', 'city', 'district', 'house_number', 'street','cep','user_image')        
    
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '''
        <span class=" form-text text-muted " >
            <small>Obrigatório. 150 caracteres ou menos. Letras, digitos e alguns caracteres</small>
        </span> 
        '''
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '''
        <ul class=" form-text text-muted small" >
            <li>Senha deve ser única.</li>
            <li>Senha deve conter pelo menos 8 caracteres.</li>
            <li>Senha deve ser totalmente numérica.</li>
        </ul> 
        '''
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a Senha'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '''
        <span class=" form-text text-muted " >
            <small>Digite a mesma senha digitada no campo anterior.</small>
        </span> 
        '''
        

# Formulário de edição de informações do usuário
class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    user_image = forms.ImageField(required=False, widget = forms.widgets.FileInput(attrs={"class":"form-control"}), label = "Imagem de Perfil:")
    cpf = forms.CharField(required=True, min_length=11, max_length=11, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cpf'}),label = "")
    bio = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Bio'}), label="Bio")

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome de usuário'}),label="Nome de usuário")
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Nova Senha'}),label='Nova Senha ( OPCIONAL )')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Senha'}),label='Confirmar Senha ( OPCIONAL )')

    state = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),label = "")
    city = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cidade'}),label = "")
    district = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bairro'}),label = "")
    house_number = forms.IntegerField(required=True,min_value=0, max_value=99999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Numero da Casa'}),label = "")
    street = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua'}),label = "")
    cep = forms.IntegerField(required=True,min_value=0, max_value=99999999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cep'}),label = "")


    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'cpf','email','password1','password2', 'user_image', 'bio', 'state', 'city', 'district', 'house_number', 'street', 'cep')   
        
        
        
# Formulário do Usuário    
class UserForm(forms.ModelForm):
    
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    user_image = forms.ImageField(required=False, widget = forms.widgets.FileInput(attrs={"class":"form-control"}), label = "Imagem de Perfil:")
    cpf = forms.CharField(required=True, min_length=11, max_length=11, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cpf'}),label = "")
    bio = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Bio'}), label="Bio")

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome de usuário'}),label="Nome de usuário")
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Nova Senha'}),label='Nova Senha ( OPCIONAL )')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Senha'}),label='Confirmar Senha ( OPCIONAL )')

    state = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),label = "")
    city = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cidade'}),label = "")
    district = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bairro'}),label = "")
    house_number = forms.IntegerField(required=True,min_value=0, max_value=99999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Numero da Casa'}),label = "")
    street = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua'}),label = "")
    cep = forms.IntegerField(required=True,min_value=0, max_value=99999999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cep'}),label = "")
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'cpf','email','password1','password2', 'bio','state', 'city', 'district', 'house_number', 'street', 'cep', 'user_image')  


        
# Formulário de Finalização de Compra
class CheckoutForm(forms.ModelForm):
    
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mail'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    cpf = forms.CharField(required=True, min_length=11, max_length=11, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cpf'}),label = "")

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome de usuário'}),label="Nome de usuário")

    state = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),label = "")
    city = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cidade'}),label = "")
    district = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bairro'}),label = "")
    house_number = forms.IntegerField(required=True,min_value=0, max_value=99999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Numero da Casa'}),label = "")
    street = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rua'}),label = "")
    cep = forms.IntegerField(required=True,min_value=0, max_value=99999999, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cep'}),label = "")
    
    total_value = forms.CharField(required=True,max_length=10, widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    
    # number_card = forms.IntegerField(required=False,min_value=0000000000000000, max_value=9999999999999999,widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'( 16 Dígitos )'}),label = "Número do Cartão")
    # name_card = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control',}), label = "Nome do Titular do Cartão" )
    # code_security_card = forms.IntegerField(required=False,min_value=000, max_value=999,widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'( 3 Dígitos )'}),label = "Código de Segurança")
    # validity_month_card = forms.IntegerField(required=False,min_value=00, max_value=12,widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'MM'}),label = "Validade (Mês)")
    # validity_year_card = forms.IntegerField(required=False,min_value=00, max_value=99,widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'AA'}),label = "Validade (Ano)")


    
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'cpf','email','state', 'city', 'district', 'house_number', 'street', 'cep', "total_value")  
        # fields = ('username','first_name','last_name', 'cpf','email','state', 'city', 'district', 
        #           'house_number', 'street', 'cep','number_card','name_card','code_security_card','validity_month_card','validity_year_card')  

    # def clean(self):
    #     cleaned_data = super().clean()
    #     payment_method = cleaned_data.get("payment")

    #     # Validação condicional para o cartão de crédito
    #     if payment_method == "cartao":
    #         # Verificar se os campos obrigatórios do cartão estão preenchidos
    #         number_card = cleaned_data.get("number_card")
    #         name_card = cleaned_data.get("name_card")
    #         code_security_card = cleaned_data.get("code_security_card")
    #         validity_month_card = cleaned_data.get("validity_month_card")
    #         validity_year_card = cleaned_data.get("validity_year_card")

    #         # Verificar se algum campo relacionado ao cartão está vazio
    #         if not number_card or not name_card or not code_security_card or not validity_month_card or not validity_year_card:
    #             raise forms.ValidationError("Todos os campos do cartão de crédito são obrigatórios.")
            
    #     return cleaned_data

    



class AddBookForm(forms.ModelForm):
    genre_choices = [
        ('','Selecione o Gênero'),
        ('Auto Ajuda', 'Auto ajuda'),
        ('Biografia', 'Biografia'),
        ('Desenvolvimento Pessoal', 'Desenvolvimento Pessoal'),
        ('Empreendedorismo', 'Empreendedorismo'),
        ('Estratégia', 'Estratégia'),
        ('Ficção', 'Ficção'),
        ('Finanças', 'Finanças'),
        ('Gestao/Lideranca', 'Gestão e Liderança'),
        ('Tecnologia', 'Tecnologia'),
    ]
    
    current_year = datetime.datetime.now().year # Pega o ano atual a partir da biblioteca datetime
    year_choices = [('','Escolha o ano ou deixe em branco para buscar automaticamente')]
    for year in range(current_year,1799, -1): # -1 é o passo negativo que faz com que a sequencia seja gerada de forma decrescente
        year_choices.append((year,year))       
    
    title = forms.CharField(required=True, widget = forms.widgets.TextInput(attrs={"placeholder":"Título Livro","class":"form-control"}), label = "")
    description = forms.CharField(required=False, widget = forms.widgets.Textarea(attrs={"placeholder":"Descrição Livro ( Deixe em branco para gerar a descrição automaticamente )","class":"form-control"}), label = "")
    # year = forms.ChoiceField(choices=year_choices,required=True, widget = forms.widgets.Select(attrs={"placeholder":"Ano Livro","class":"form-control", "id":"field_year"}), label = "")

    year = forms.ChoiceField(choices=year_choices,required=False, widget=forms.widgets.Select(attrs={"placeholder": "Ano Livro (Deixe em Branco para Buscar o Ano Automaticamente)", "class": "form-control js-example-tokenizer", "id": "field_year"}), label = "")
    
    # genre = forms.CharField(required=True, widget = forms.widgets.TextInput(attrs={"placeholder":"Gênero Livro","class":"form-control"}), label = "")

    # genre = forms.TagField(choices = genre_choices, required=True, widget=forms.widgets.Select(attrs={"placeholder":"Gênero Livro","class":"form-control"}), label = "")
    genre = forms.ChoiceField(choices = genre_choices, required=True, widget=forms.widgets.Select(attrs={"placeholder":"Gênero Livro","class":"form-control"}), label = "")
    # tags = forms.
    
    value = forms.FloatField(required=True, min_value=0, widget = forms.widgets.NumberInput(attrs={"placeholder":"Valor Livro","class":"form-control"}), label = "")
    stock = forms.IntegerField(required=True, min_value=0, widget = forms.widgets.NumberInput(attrs={"placeholder":"Estoque","class":"form-control"}), label="")
    image = forms.ImageField(widget = forms.widgets.FileInput(attrs={"class":"form-control"}), label = "Imagem")
    
    class Meta:
        model = Book
        fields = ('title', 'description', 'year', 'genre', 'value','stock','image')

    # Converte vazio em None caso não for passado o valor do ano do livro
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year == '':
            return None  # importante: converte string vazia para None
        return int(year) 
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # Passa uma lista de opções (datalist) para o campo year que tem Auto complete
        self.fields['year'].widget.attrs['list'] = 'year_choices'
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    
    # Campos preenchidos automaticamente:
    book = forms.ModelChoiceField(queryset=Book.objects.all(),widget=forms.HiddenInput(), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput(), required=False)

    # Campo de comentário preenchido pelo usuário:
    text = forms.CharField(
        required=True, 
        widget = forms.Textarea(attrs={"placeholder":"Adicione um comentário. (Limite de 300 caracteres)","class":"form-control"}), 
        label = "", 
        max_length=300) # Limita o numero de caracteres a serem digitados.



class RatingForm(forms.ModelForm):
    class Meta:
        model = RatinStar
        fields = ['rating']
        
    # Campos preenchidos automaticamente:
    book = forms.ModelChoiceField(queryset=Book.objects.all(),widget=forms.HiddenInput(), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput(), required=False)
    
    # Campo de avaliação "Estrelas" preenchido pelo usuário:
    rating = forms.DecimalField(required=True,min_value=1,max_value=5,widget=forms.RadioSelect(choices=[(i,str(i)) for i in range(1,6)]))








    # Possibilita usar o mesmo nome de usuário
    # def clean_username(self):
    #     username = self.cleaned_data.get('username') # Pega o novo valor do nome de usuário digitado no formulário.
    #     user = self.instance  # Usuario atual ( LOGADO )

    #     # Se o valor no campo de nome de usuario for igual ao nome do usuario logado, retorna o nome atual
    #     if username == user.username:
    #         return username
        
    #     # Se o nome de usuario for alterado, veifica se ja existe no banco de dados
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("Esse nome de usuário já está em uso.")
            
    #     return username     
    
    # Possibilita usar a mesma senha anterior
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
        
    #     if password1 or password2:
    #         if password1 != password2:
    #             raise ValidationError("As senhas não coincidem.")
    #         if len(password1) < 8 or len(password2) < 8:
    #             raise ValidationError("A senha deve ter pelo menos 8 caracteres")
    #         if password1.is_digit() or password2.is_digit():
    #             raise ValidationError("A senha não pode ser totalmente numérica")
    #         return password2
        
        
    # def save(self, commit=True):
    #     user = super(ProfileForm, self).save(commit=False)
        
    #     # Se uma nova senha foi fornecida, alteramos a senha do usuario
    #     if self.cleaned_data.get('password1'):
    #         user.set_password(self.cleaned_data['password1'])

    #     if commit:
    #         user.save()

    #     user_profile = UserProfile.objects.filter(user=user).first()
    #     if user_profile:
    #         user_profile.cpf = self.cleaned_data.get('cpf')
    #         user_profile.user_image = self.cleaned_data.get('user_image')
    #         user_profile.save()
    #     return user