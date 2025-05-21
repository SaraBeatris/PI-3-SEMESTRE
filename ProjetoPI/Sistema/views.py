from django.shortcuts import render, redirect
from .forms import User, CadastroRestauranteForm, ColaboradorForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile

def home(request):
    return render (request, 'home.html')


def login(request):
    return render(request, 'login.html')


def cadastro_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastro_colaborador')  
    else:
        form = ColaboradorForm()

    return render(request, 'cadastro.html', {'form': form})


def cadastroRestaurante(request):
    if request.method == 'POST':
        form = CadastroRestauranteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurante cadastrado com sucesso!')
            return redirect('login')  # Redireciona após sucesso
    else:
        form = CadastroRestauranteForm()

    return render(request, 'cadastroRestaurante.html', { 'form': form})
                  
logger = logging.getLogger(__name__)
# Senha fornecida pelo rh
ADMIN_PASSWORD = "Senha123"

def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        tipo = request.POST.get('tipo')
        admin_password = request.POST.get('admin_password', '')
        
        # Validação básica
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastrar_usuario')
        
        # Verificação para cadastro de admin
        if tipo == 'admin':
            if admin_password != ADMIN_PASSWORD:
                messages.error(request, 'Senha de administrador incorreta!')
                return redirect('cadastrar_usuario')
            
            # Log de criação de admin
            logger.info(f'Novo admin criado por {request.user.username}: {username}')
            messages.success(request, 'Administrador criado com sucesso! Registro de auditoria gerado.')
        
        try:
            # Cria o usuário
            user = User.objects.create_user(username, email, password)
            
            # Adiciona ao grupo conforme o tipo
            if tipo == 'admin':
                group = Group.objects.get(name='Administradores')  # Certifique-se que o grupo existe
                user.is_staff = True
            else:
                group = Group.objects.get(name='Encarregados')  # Certifique-se que o grupo existe
            
            user.groups.add(group)
            user.save()
            
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('cadastrar_usuario.html')  # Redirecione para onde for apropriado
            
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    return render(request, 'cadastrar_usuario.html')  # Substitua pelo seu template



