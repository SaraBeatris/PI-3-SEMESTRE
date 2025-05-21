from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Restaurante, Colaborador, Profile

# Cadatro restaurantes 
# class CadastroRestauranteForm(Restaurante):
        
class CadastroRestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'responsavel', 'capacidade', 'avaliacao', 'ativo']


# Cadatro usuarios 
# Cadatro usuarios 
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail"
    )

    tipo = forms.ChoiceField(
        choices=Profile.TIPOS_USUARIO,
        label="Tipo de Usuário",
        required=True,
        widget=forms.Select(attrs={'onchange': 'toggleAdminPassword()'})
    )

    telefone = forms.CharField(
        max_length=15,
        required=False,
        label="Telefone"
    )

    admin_password = forms.CharField(
        required=False,
        label="Senha de Administrador (fornecida pelo RH)",
        widget=forms.PasswordInput(attrs={'style': 'display: none;'}),
        help_text="Obrigatório apenas para cadastro de administradores"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tipo', 'telefone', 'admin_password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Se o usuário atual não for admin, remova a opção de admin
        if self.request and not self.request.user.is_superuser:
            self.fields['tipo'].choices = [
                (value, label) for value, label in Profile.TIPOS_USUARIO 
                if value != 'admin'
            ]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        admin_password = cleaned_data.get('admin_password')
        
        # Validação para cadastro de administrador
        if tipo == 'admin':
            # Obtenha a senha de admin das variáveis de ambiente
            rh_admin_password = "Senha123" 
            
            if not admin_password:
                raise ValidationError("Senha de administrador é obrigatória para este tipo de usuário")
            
            if admin_password != rh_admin_password:
                raise ValidationError("Senha de administrador incorreta")
            
            # Registro de auditoria
            if self.request:
                user = self.request.user
                print(f"Auditoria: Usuário {user.username} tentou criar um admin")  # Substitua por um logger real

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Se for admin, define como superuser/staff
        if self.cleaned_data['tipo'] == 'admin':
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()
            
            Profile.objects.create(
                user=user,
                tipo=self.cleaned_data['tipo'],
                telefone=self.cleaned_data.get('telefone')
            )

        return user
        
class ColaboradorForm(forms.ModelForm):
    class Meta: 
        model = Colaborador
        fields = [
            'nome', 'cpf', 'rg', 'data_nascimento', 'sexo', 'estado_civil', 'telefone',
            'telefone_emergencia', 'cep', 'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'estado', 'funcao', 'salario', 'data_admissao', 'data_demissao',
            'obra', 'ativo', 'foto', 'observacoes'
        ]
