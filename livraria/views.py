from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import SignUpForm, AddBookForm, CommentForm, RatingForm, ProfileForm, UserForm, CheckoutForm
from .models import Book, Comment, RatinStar, UserProfile, FriendRequest
from django.template.loader import render_to_string
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
import requests


# Função para calcular a avaliação geral por estrelas
def calculate_media_rating(book):
    overall_rating = RatinStar.objects.filter(book=book) # pega as avaliações por livro (Query set)
    total_n_rating = 0 
    total_rating = 0 
    for item in overall_rating:
        total_rating += item.rating
        total_n_rating += item.n_review            
    # print(f"Esse é o total N rating {total_n_rating}")
    # print(f"Esse é o total rating {total_rating}")
    
    if overall_rating:
        media_rating = total_rating / total_n_rating
        media_rating = round(media_rating,1)
        # print(f"Esse é o media rating {media_rating}")
    else:
        media_rating = 0
    return media_rating


def login_user(request):
    if request.method == "POST":
        username = request.POST['usuario'] # Pega o usuario atraves do atributo name do input do html 
        password = request.POST['senha'] # Pega o usuario atraves do atributo name do input do html 
        
        user = authenticate(
            request,
            username = username,
            password = password
        )
        
        if user is not None:
            login(request,user)
            messages.success(request, f'Olá {user.username}, Seja Bem Vindo! ')
            return redirect('home')
        else:
            messages.error(request,"Erro na autenticação. Tente novamente!")
            return redirect('login')
    return render(request, 'login.html')



def home(request):
    books = Book.objects.all().order_by('-media_rating') # Ordena em ordem alfabetica pelo titulo

    if request.user.is_authenticated:

        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)

        return render(request, 'home.html',{'books':books,'friend_requests':friend_requests,})
    
    else:

    # book_id = Book.objects.get(id =id)
    # media_rating = calculate_media_rating(book_id)
    
    # for book in books:
    #     media_rating = calculate_media_rating(book)





        # Se eu fizer uma requisição do tipo post:

        # if request.method == "POST":
        #     username = request.POST['usuario'] # Pega o usuario atraves do atributo name do input do html 
        #     password = request.POST['senha'] # Pega o usuario atraves do atributo name do input do html 
            
        #     user = authenticate(
        #         request,
        #         username = username,
        #         password = password
        #     )
            
        #     if user is not None:
        #         login(request,user)
        #         messages.success(request, f'Olá {user.username}, Seja Bem Vindo! ')
        #         return redirect('home')
        #     else:
        #         messages.error(request,"Erro na autenticação. Tente novamente!")
        #         return redirect('home')
            
        # Se eu não realizei nenhuma requisição e ja estou autenticado, vai para o else (vai para a home)
        # else:
        return render(request, 'home.html',{'books':books})



def logout_user(request):
    logout(request)
    messages.success(request,"Você fez logout")
    return redirect('home')



def resize_profile_image(image):
    img = Image.open(image)
    
    original_width, original_height = img.size # index 0 é a largura, index 1 é a altura         
    shortest_side = min(original_width, original_height)
    
    # Definição dos tamanhos para centralizar o corte da imagem (Para não ficar com as laterais pretas)
    left = (original_width - shortest_side) // 2

    if original_height > 1500: # Se a imagem for maior que 1500 px, joga a imagem 450 px para baixo para cortar
        top = (original_height - shortest_side) // 2 - 450
    else:
        top = (original_height - shortest_side) // 2 # Centraliza a imagem para cortar
        
    top = max(top,0) # garante que o valor de top nunca seja negativo, evitando que o corte vá para fora da parte superior da imagem.
    right = left + shortest_side
    bottom = top + shortest_side
    
    img = img.crop((left,top,right,bottom)) # Corte da imagem

    img_io = BytesIO()  # cria um arquivo simulado na memória (em vez de um arquivo físico) para ser manipulado sem precisar gravá-lo em disco
    img.save(img_io, format="JPEG") # salva no formato jpeg
    img_io.seek(0)  # seek(0) basicamente "prepara" o fluxo de bytes para ser lido a partir do início após salvar a imagem

    # Cria um arquivo simulado (objeto) em memória (usando o InMemoryUploadedFile) a partir do objeto img_io que pode ser tratado como um arquivo real, mas sem ser armazenado no disco.
    image_file = InMemoryUploadedFile(img_io, None, image.name, 'image/jpeg', sys.getsizeof(img_io),None)    
    
    
    # ARGUMENTOS PASSADOS PARA O InMemoryUploadedFile:
    
    # img_io: Este é o fluxo de bytes que contém os dados da imagem (que foi salva anteriormente com img.save(img_io, format="JPEG")). 
    # Esse fluxo de bytes é o "conteúdo" do arquivo simulado.

    # None: O segundo argumento é o campo field_name, que é utilizado para referenciar o nome do campo no qual o arquivo seria enviado 
    # em um formulário de upload. Nesse caso, não está sendo utilizado, então é passado None.

    # image.name: Este é o nome original do arquivo de imagem (o nome da imagem que foi passada para a função). 
    # Ele será usado para simular o nome do arquivo ao ser armazenado como um arquivo em memória.

    # 'image/jpeg': O tipo MIME (ou content type) do arquivo. Neste caso, a imagem é salva no formato JPEG, 
    # então é passado 'image/jpeg' para indicar isso. É importante para que os sistemas que utilizem esse arquivo saibam qual o tipo de conteúdo.

    # sys.getsizeof(img_io): Esse argumento especifica o tamanho do arquivo em bytes. sys.getsizeof(img_io) retorna o 
    # número de bytes ocupados pelo objeto img_io (a imagem redimensionada em memória). Isso é necessário para que 
    # o Django ou outro sistema que manipula esse arquivo saiba quanto espaço ele ocupa.

    # None: O último argumento é o campo charset, que, em geral, é utilizado para arquivos de texto. 
    # Nesse caso, como estamos lidando com uma imagem, o valor é None.
    
    return image_file



# Função para cadastrar um novo usuario, após cadastrar o usuario ja é logado automaticamente
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES) # vai passar os dados da requisição via post para a variavel form
        if form.is_valid():
            
            # form.save() # Registra o usuário no banco de dados, criando o novo usuário.
            user = form.save() # Salvando o objeto usuario na variavel user para utilizar na variavel user user_profile
            user_image = form.cleaned_data['user_image']
            cpf = form.cleaned_data['cpf']
            bio = form.cleaned_data['bio']
            
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            street = form.cleaned_data['street']
            house_number = form.cleaned_data['house_number']
            cep = form.cleaned_data['cep']
            
            if user_image:
                user_image = resize_profile_image(user_image)
                user_profile = UserProfile.objects.create(user = user, user_image = user_image, cpf = cpf, bio = bio,
                                                          state=state,city=city,district=district,street=street,house_number=house_number,cep=cep)
            else:
                # user_profile = UserProfile.objects.create(user = user,  user_image = "../../media/users/default.jpg" , cpf = cpf)
                user_profile = UserProfile.objects.create(user = user,  user_image = "users/default.jpg" , cpf = cpf, bio=bio,
                                                          state=state,city=city,district=district,street=street,house_number=house_number,cep=cep)
                
            user_profile.save()            
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']                       
            
            # EXPLICAÇÃO DO METODO CLEANED_DATA:
            
            # Quando você chama form.is_valid(), o Django valida todos os campos do formulário e, caso estejam 
            # corretos, os armazena em um dicionário chamado cleaned_data.
            
            # Após a validação, form.cleaned_data contém os valores finais e seguros que o usuário forneceu. Então, as linhas:
                # username = form.cleaned_data['username']
                # password = form.cleaned_data['password1']
            # estão extraindo os valores validados para usá-los em outro contexto, como, neste caso, para autenticar o usuário.
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Você fez login com sucesso com o novo usuário!")
                return redirect('home')
            else:
                messages.error(request, "Erro na autenticação. Tente novamente.")
                return redirect('register')
        
    # O else é usado apenas para exibir o formulário vazio quando a página de registro é carregada pela primeira vez ou após um erro na validação do formulário.
    else:
        form = SignUpForm()
        return render (request,'register.html',{'form':form})
    return render (request,'register.html', {'form':form})


def profile_user_view(request, id):
    if request.user.is_authenticated:     
        
        books = Book.objects.all()

        user_logged = request.user  # Usuário logado
        user_profile = get_object_or_404(User, id=id)  # Usuário visitado
        user_profile_instance = get_object_or_404(UserProfile, user=user_profile)  # Usuário visitado ( Usado para mostar a bio pegando o id do usuario visitado )
        
        ratings = RatinStar.objects.filter(user=user_profile, rating__gte=4.0).order_by('-rating') # rating__gt=4 filtra os ratings que são maiores que 4. O __gt é um lookup do Django que significa "maior que" (greater than).

        # /////////////////////////////////////////////////////////////////////////////////////////////
        # TESTE
        
        # ratings = RatinStar.objects.filter(user=user_profile) # Avaliações feita pelo usuário
        # print(ratings)
        
        # last_ratings = {} # Avaliações recentes e sem repetições

        # for rating in ratings: # Pega todas as avaliações feitas
        #     book_id = rating.book.id
            
        #     last_ratings[book_id] = rating # Passa a ultima avaliação com rating superior a 4 e envia para o last_ratings
            
        #     # if rating.rating >= 4:
        #     #     last_ratings[book_id] = rating # Passa a ultima avaliação com rating superior a 4 e envia para o last_ratings

        # print("Esse é o last ratings",last_ratings)
        
        # last_ratings_list = list(last_ratings.values())
        # print("Esse é o last ratings LIST",last_ratings_list)
        
        # /////////////////////////////////////////////////////////////////////////////////////////////
        
        
        # Remover avaliações duplicadas por livro ( Não da pra fazer com set pois se não vai ser perdido as propriedades de busca )
        unique_ratings = []
        seen_books = set()
        for rating in ratings:
            if rating.book not in seen_books: # Se o livro não existe em seen_books (livros vistos)
                unique_ratings.append(rating)
                seen_books.add(rating.book) # adiciona a livros vistos impedindo que ocorra repetições de itens
            if len(unique_ratings) == 5:
                break
            
        # Remover generos repetidos
        unique_genres = set()
        for rating in ratings:
            unique_genres.add(rating.genre)      
            
            
        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)

        # Verifica se existe solicitação de amizade
        friend_request_solicitation = FriendRequest.objects.filter(from_user=user_logged, to_user=user_profile).exists()
        
        # Verificar Seguidores do perfil do usuario visitado: 
        is_follower = user_logged.userprofile.followers.filter(id=user_profile_instance.id).exists()     
        
        # Verificar quem o usuario que tem o perfil visitado segue: 
        is_following = user_profile.userprofile.following.all()
        # print("is_following: ",is_following) # mostra um objeto do tipo queryset
        
        # Filtra se o usuario logado segue o usuario visitado
        # is_following_filter = user_logged.userprofile.following.filter(user=user_logged).exists()
        is_following_filter = user_logged.userprofile.following.filter(id=user_profile_instance.id).exists()

        # print("TESTE DE QUEM EU SIGO ")
        # for user_following in is_following:
        #     print(user_following.user.username)
        
        # Solicitação de amizade
        if request.method == 'POST':           
            
            if 'friend_request' in request.POST:                
                user_logged_profile = get_object_or_404(UserProfile, user=request.user)
                user_logged_profile.send_friend_request(user_profile_instance)   
                print("Solicitação Enviada")
                messages.success(request, f"Solicitação para {user_profile_instance.user.username} enviada com sucesso.")
                return redirect('profile_view', id=user_profile.id)
                
            if 'remove_follower' in request.POST:
                user_logged_profile = get_object_or_404(UserProfile, user=request.user)
                user_logged_profile.remove_follower(user_profile_instance)
                messages.success(request, f"Voce removeu {user_profile_instance.user.username} .")
                print("Remove FOLLOWER")              
                return redirect('profile_view', id=user_profile.id)
            
            if 'unfollow' in request.POST:
                user_logged_profile = get_object_or_404(UserProfile, user=request.user)
                user_logged_profile.unfollow(user_profile_instance)
                messages.success(request, f"Voce deixou de seguir {user_profile_instance.user.username} .")
                print("UNFOLLOW")              
                return redirect('profile_view', id=user_profile.id)
        
        return render(request, 'profile_view.html', {
            'user_logged': user_logged,  # usuário logado 
            'user_profile': user_profile,  # Usuário que está sendo visitado
            'user_profile_instance':user_profile_instance, # usado para passar a bio do usuario visitado para o template
            # 'last_ratings_list': last_ratings_list,
            "ratings": unique_ratings,
            "books": books,
            "unique_genres": unique_genres,
            "friend_requests":friend_requests,
            "is_follower":is_follower,
            "is_following":is_following,
            "is_following_filter": is_following_filter,
            "friend_request_solicitation": friend_request_solicitation,
        })
    else:
        return redirect('home')
    
    
def  accept_friend_request(request, id):
    friend_request = get_object_or_404(FriendRequest, id=id)
    friend_request.accepted = True # Aceita a solicitação de amizade
    friend_request.save()
    
    # Adiciona os amigos na lista de amizade
    from_user_profile = get_object_or_404(UserProfile, user=friend_request.from_user)
    to_user_profile = get_object_or_404(UserProfile, user = friend_request.to_user)

    to_user_profile.accept_friend_request(from_user_profile)
    friend_request.delete() # Exclui a solicitação de amizade

    messages.success(request, f"Você aceitou a solicitação de amizade de {friend_request.from_user.username}")
    return redirect('profile_view', id=friend_request.to_user.id)


def reject_friend_request(request, id):
    friend_request = get_object_or_404(FriendRequest, id=id)
    friend_request.rejected = True # Rejeita a solicitação de amizade
    friend_request.save()
    friend_request.delete()
    messages.success(request, f"Você recusou a solicitação de amizade de {friend_request.from_user.username}")
    return redirect('profile_view', id=friend_request.to_user.id)

    
    
def profile_user_edit(request):
    if request.user.is_authenticated:        
        # user = request.user
        profile = get_object_or_404(UserProfile, user=request.user)  # Cria um objeto do modelo do usuario  

        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
            
        if request.method == 'POST':
            profileForm = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
            # profileForm = ProfileForm(request.POST or None, request.FILES or None, instance=user) # Não aceita o usuario logado como instancia
            userForm = UserForm(request.POST, instance=request.user  )
        else:
            profileForm = ProfileForm(instance=profile)
            # profileForm = ProfileForm(instance=user) # Não aceita o usuario logado como instancia
            userForm = UserForm(instance=request.user  )
            
        if profileForm.is_valid() and userForm.is_valid():            
            user_image = profileForm.cleaned_data['user_image']

            if user_image:
                user_image = resize_profile_image(user_image)
                profile.user_image = user_image # Passa a imagem editada pela função resize_profile_image() para o profile antes de salvar o formulário
                
            profileForm.save()
            userForm.save()
            
            messages.success(request, "Perfil Atualizado!")
            return redirect('profile_view', id=request.user.id)
        else:
            if request.method == 'POST':
                messages.error(request,'Erro ao atualizar o perfil. Tente novamente.')
        return render(request, 'profile_edit.html', {
            'profileForm': profileForm,
            "friend_requests":friend_requests,
            'userForm': userForm,
        })

    else:
        return redirect('home')
    
    
    
    


# Só vai acessar os detalhes do livro se estiver autenticado
def book_detail(request, id):
    book = Book.objects.get(id =id)
    # user_image_profile = UserProfile.objects.get(id = id)
    
    if request.user.is_authenticated:        
        comment_form = CommentForm()  # Inicializando os formulários fora do bloco POST pra não dar erro nos comentarios e no ratingStar
        rating_form = RatingForm() # Inicializando os formulários fora do bloco POST pra não dar erro nos comentarios e no ratingStar
        comments = book.comments.all().order_by('-date') # Ordena os comentário mais recentes no topo
        
        ratings = RatinStar.objects.filter(user = request.user, book = book)

        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        
        # if ratings:
            # user_rating = ratings.last() if ratings.exists() else None # Pega a última avaliação do usuário
        user_rating = ratings.last() if ratings.exists() else None # Pega a última avaliação do usuário
        
        # ///////////////////////////////////////////////////////////////////////////
        # AVALIAÇÃO GERAL DO LIVRO POR ESTRELAS:                
        media_rating = calculate_media_rating(book)
        
        if request.method == "POST":            
            
            # ///////////////////////////////////////////////////////////////////////////
            # DELETAR COMENTÁRIO:
            delete_comment_id = request.POST.get('delete_comment')
            if delete_comment_id:
                comment = get_object_or_404(Comment, id = delete_comment_id) # se o objeto não for encontrado, ele automaticamente gera um erro 404, sem você precisar lidar com a exceção manualmente.

                if request.user == comment.user or request.user.is_staff:
                    comment.delete()
                    messages.success(request, 'Comentário excluído com sucesso!')
                else:
                    messages.error(request,'Você não tem permissão para excluir o comentário!')            
            
            
            # ///////////////////////////////////////////////////////////////////////////
            # ADICIONAR COMENTÁRIO:
            if 'comment_submit' in request.POST: # Nome do botão de envio do formulário = 'comment_submit'
                comment_form = CommentForm(request.POST) # variavel comment_form recebe o valor do formulário de requisição
                if comment_form.is_valid():
                    
                    # ( comment = comment_form.save(commit=False) ) "Salva" o formulário sem enviar ao banco de dados "sem fazer o commit", 
                    # o que permite adicionar as  informações extras (como o livro e o usuário) para depois salvar e enviar ao banco de dados. 
                    # (Estou criando um objeto comment que recebe as informações do formulario, vou poder adicionar mais informações para salvar e enviar ao banco de dados )
                    comment = comment_form.save(commit=False) 
                    
                    comment.book = book
                    comment.user = request.user
                    comment.save()
                    
                    messages.success(request, 'Comentário adicionado com sucesso!')
                    comment_form = CommentForm() # Limpa os dados do campo de comentários após o envio (Cria uma nova instancia do formulário)
                    
                    
                    return render(request, 'book.html', {'book':book, 'comments': comments, 'comment_form':comment_form,})             
            
            
            # ///////////////////////////////////////////////////////////////////////////
            # ADICIONAR AVALIAÇÃO:
            if 'rating_submit' in request.POST: # Nome do botão de envio do formulário = 'rating_submit'           
                
                rating_value = request.POST.get('rating') # Pega o valor do input através do name 'rating' do input
                rating_value = int(rating_value) # Passa para int pra comparar no if abaixo
                if rating_value and rating_value >= 1 and rating_value <= 5:
                # if rating_value :
                    rating_form = RatingForm(request.POST) 
                    if rating_form.is_valid():
                        rating = rating_form.save(commit=False)
                        
                        rating.book = book
                        rating.user = request.user
                        rating.value = int(rating_value)
                        rating.n_review = 1               # SALVA o numero de avaliadores
                        rating.genre = book.genre
                        rating.save()
                        media_rating = calculate_media_rating(book) # Atualiza a avaliação geral do livro ao enviar a nota de avaliação

                        book.media_rating = media_rating # Salva a media da avaliação geral do livro no modelo do livro
                        book.save()
                        user_rating = rating # Atualiza o rating star apos a avaliação do formulário para renderizar na pagina
                        print(f"Depois de salvar: media_rating = {media_rating}, book.media_rating = {book.media_rating}")
                        messages.success(request, 'Avaliação enviada com sucesso!')
                    else:
                        messages.error(request,"Erro ao enviar a avaliação")
                        # return render(request, 'book.html', {'book':book, 'comments': comments, 'comment_form':comment_form,'media_rating': media_rating})   
                        # return render(request, 'book.html', {'book':book, 'media_rating': media_rating, }) 
                        
                        return render(request, 'book.html', {
                            'book':book, 'media_rating': media_rating,
                            'comments': comments, 'comment_form':comment_form, # Envia comments e comment_form para renderizar o campo de comentário
                            'user_rating': user_rating if user_rating else None }) 
                        
                        # return redirect('book.html', id=book.id)                
   
        # return render(request, 'book.html', {'book':book, 'comment_form':comment_form, 'rating_form': rating_form, 'media_rating': media_rating,'comments': comments,  })  # {'book': book} é um dicionário sendo passado para o contexto da página que será renderizada.
        return render(request, 'book.html', {
            'book':book, 
            'comment_form':comment_form, 
            'rating_form': rating_form, 
            'media_rating': media_rating,
            'comments': comments, 
            "friend_requests":friend_requests,
            'user_rating': user_rating if user_rating else None })  # {'book': book} é um dicionário sendo passado para o contexto da página que será renderizada.
    else:
        messages.warning(request, 'Faça Login ou Cadastre-se agora mesmo, é rapido!')
        return redirect('home')



# Só vai deletar o livro se estiver autenticado
def book_delete(request,id):
    if request.user.is_authenticated:
        book = Book.objects.get(id = id)
        book.delete()
        
        # //////////////////////////////////////////////////////////////////////////////////////////////////////
        # //////////////// Remove o cadastro do livro no banco de dados da API ////////////////////////
        
        book_title = book.title
        
        # get_id_bookDB_API = requests.get(f'http://localhost:8080/api/v1/books/?title={book_title}')
        get_id_bookDB_API = requests.get(f'http://localhost:8080/api/v1/books/', json= {"title":book_title})
        print("Teste get_id_bookDB_API: ",get_id_bookDB_API)
        
        if get_id_bookDB_API.status_code == 200:
            book_data = get_id_bookDB_API.json()
            
            for item in book_data:
                if item['title'] == book_title:
                    object_API_to_delete = item
                    
            print("Esse é o object_API_to_delete: ", object_API_to_delete)
            
            id_delete = object_API_to_delete["id"]

        else:
            print("Erro ao buscar Livro: ", get_id_bookDB_API.status_code, get_id_bookDB_API.text)
            
            
        
        send_response = requests.delete(f'http://localhost:8080/api/v1/books/{id_delete}/')
        
        if send_response.status_code == 200:
            print("Livro cadastrado na api com sucesso!", send_response.json())
        else:
            print("Erro:", send_response.status_code, send_response.text)
            
        # //////////////////////////////////////////////////////////////////////////////////////////////////////
        # //////////////////////////////////////////////////////////////////////////////////////////////////////
        
        
        messages.success(request, "Livro excluído com sucesso!")
        return redirect('home')
    else:
        messages.error(request,'Voce precisa estar logado!')
        return redirect('home')



def resize_image_book(image, size=(400,300)):
    img = Image.open(image)
    
    original_width, original_height = img.size # index 0 é a largura, index 1 é a altura         
    shortest_side = min(original_width, original_height) # Pega o menor dos lados
    
    # Se largura for maior que altura
    if original_width > original_height:
        
        # Definição dos tamanhos para centralizar o corte da imagem (Para não ficar com as laterais pretas)
        left = (original_width - shortest_side) // 2
        top = (original_height - shortest_side) // 2 
        top = max(top,0) # garante que o valor de top nunca seja negativo, evitando que o corte vá para fora da parte superior da imagem.
        right = left + shortest_side
        bottom = top + shortest_side
    
        img = img.crop((left,top,right,bottom)) # Corte da imagem
        
    # Se altura for maior que largura
    elif original_width < original_height:        
        width_ratio  = size[0] / original_width
        height_ratio  = size[1] / original_height     
        ratio  = min(width_ratio, height_ratio)    
            
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        print(f"Redimensionando para: {new_width}x{new_height}")        
        img = img.resize((new_width, new_height), Image.LANCZOS)
        

    img_io = BytesIO()  # cria um arquivo simulado na memória (em vez de um arquivo físico) para ser manipulado sem precisar gravá-lo em disco
    img.save(img_io, format="JPEG") # salva no formato jpeg
    img_io.seek(0)  # seek(0) basicamente "prepara" o fluxo de bytes para ser lido a partir do início após salvar a imagem

    # Cria um arquivo simulado (objeto) em memória (usando o InMemoryUploadedFile) a partir do objeto img_io que pode ser tratado como um arquivo real, mas sem ser armazenado no disco.
    image_file = InMemoryUploadedFile(img_io, None, image.name, 'image/jpeg', sys.getsizeof(img_io),None)    
    
    return image_file
    



def book_add(request):
    form = AddBookForm(request.POST or None, request.FILES or None ) # Se não tiver nenhuma requisição o valor de form vai ser none
    
    if request.user.is_authenticated: # Se o usuario estiver autenticado
        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)

        if request.method == "POST": # se o metodo da requisição for igual a post
            if form.is_valid(): # se todos os dados do formulário forem validos
                image = request.FILES.get('image')
                if image:
                    image = resize_image_book(image)
                    form.instance.image = image
                book = form.save() # salva o formulário
                
                genre_tag = form.cleaned_data['genre']
                
                # book = Book.objects.get(id=1)
                # book.tags.add("Ficção", "Tecnologia")  # Adicionando várias tags

                
                book.tags.add(genre_tag)
                # tag, created = Tag.objects.get_or_create(name=genre_tag)
                # book.tags.add(tag)
                print(book)
                print(book.tags.all())
                
                # //////////////////////////////////////////////////////////////////////////////////////////////////////
                # //////////////// Cadastro de titulo e valor do livro no banco de dados da API ////////////////////////
                
                data = {
                    "title":book.title,
                    "total_value":book.value,
                }
                
                send_response = requests.post('http://localhost:8080/api/v1/books/', json=data)
                
                if send_response.status_code == 200:
                    print("Livro cadastrado na api com sucesso!", send_response.json())
                else:
                    print("Erro:", send_response.status_code, send_response.text)
                    
                # //////////////////////////////////////////////////////////////////////////////////////////////////////
                # //////////////////////////////////////////////////////////////////////////////////////////////////////
                
                messages.success(request, "Livro adicionado com sucesso")
                return redirect('home') # redireciona para a home            
        # return render(request, 'add_book.html', {'form':form, 'year_choices': year_choices,})
        return render(request, 'add_book.html', {'form':form,'friend_requests':friend_requests,})
    
    # EXPLICAÇÃO:
    # render(request, 'add_book.html'): Acontece quando:
    #     O usuário está autenticado e a requisição é GET (primeira vez que acessa a página).
    #     O formulário ainda não foi enviado.
    # redirect('home'): Acontece quando:
    #     O usuário está autenticado e o formulário foi enviado e validado (requisão POST).
    #     O usuário não está autenticado, e uma tentativa de adicionar o livro é feita (isso ocorre imediatamente após a verificação de autenticação). 
    #     O código redireciona o usuário para a página inicial (home).
        
    else: # Se o usuário não estiver autenticado
        messages.error(request, 'Voce deve estar autenticado para adicionar o livro!')
        return redirect('home')   
    
    

def book_update(request,id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        # print(book)
        book.last_update = timezone.now()
        form = AddBookForm(request.POST or None, instance=book) # (request.POST or None) Se não tiver nenhuma requisição o valor de form vai ser none
        # (Instance=book)  o formulário será pré-preenchido com os dados do livro clicado/escolhido
        
        if form.is_valid():
            form.save()
            
            # //////////////////////////////////////////////////////////////////////////////////////////////////////
            # //////////////// Atualiza o cadastro do livro no banco de dados da API ////////////////////////
            
            book_title = book.title
            book_value = book.value
            
            get_id_bookDB_API = requests.get(f'http://localhost:8080/api/v1/books/', json= {"title":book_title}) # Busca o livro a ser atualizado na API pelo título
            print("Teste get_id_bookDB_API: ",get_id_bookDB_API)
            
            if get_id_bookDB_API.status_code == 200:
                book_data = get_id_bookDB_API.json()
                
                for item in book_data:
                    if item['title'] == book_title:
                        object_API_to_update = item
                        
                print("Esse é o object_API_to_update: ", object_API_to_update)
                
                id_update = object_API_to_update["id"]
            else:
                print("Erro ao buscar Livro: ", get_id_bookDB_API.status_code, get_id_bookDB_API.text)
                
            data = {"title":book_title, "total_value": book_value}
            
            send_response = requests.put(f'http://localhost:8080/api/v1/books/{id_update}/', json= data)
            
            if send_response.status_code == 200:
                print("Livro cadastrado na api com sucesso!", send_response.json())
            else:
                print("Erro:", send_response.status_code, send_response.text)
                
            # //////////////////////////////////////////////////////////////////////////////////////////////////////
            # //////////////////////////////////////////////////////////////////////////////////////////////////////
            
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('home')
        
        return render(request,'update_book.html', {'form':form})
    else:
        messages.error(request, 'Voce deve estar autenticado para atualizar o livro!')
        
        
        
def book_search(request):
    if request.user.is_authenticated:
        search_term = request.GET.get('search')     
        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
   
        if search_term:
            books = Book.objects.filter(title__icontains = search_term) # Filtra os livros pelo título         
        else:
            return redirect('home')
            # books = Book.objects.all() # Se não houver termo de busca, mostra todos os livros    
    else:
        # books = [] # quando o usuário não está autenticado (else: books = []) vai garantir que nenhum livro será mostrado na página de busca.
        return redirect('home')
        
    return render(request, 'search.html',{'books':books,'friend_requests':friend_requests,})






def tag_search(request):
    if request.user.is_authenticated:
        search_term = request.GET.get('search')

        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        
        if search_term:
            books = Book.objects.filter(tags__name__icontains=search_term) # Filtra as tags pelo nome         
            
        else:
            return redirect('home')
            # books = Book.objects.all() # Se não houver termo de busca, mostra todos os livros
    
    else:
        # books = [] # quando o usuário não está autenticado (else: books = []) vai garantir que nenhum livro será mostrado na página de busca.
        return redirect('home')
        
    return render(request, 'search.html',{'books':books,'friend_requests':friend_requests,})



# Apenas carrega as informações na pagina de checkout
def page_checkout(request):
    if request.user.is_authenticated:
        # profile = get_object_or_404(UserProfile, user=request.user)  # Cria um objeto do modelo do usuario  
        # user_logged = get_object_or_404(UserProfile, user=request.user)  # Usuário logado
        user_logged = request.user

        # user = request.user
        # profile = get_object_or_404(UserProfile, user = user)
        profile = get_object_or_404(UserProfile, user=user_logged)

        # Preenche os dados do formulario de compra 
        initial_data = {
            'state': profile.state,
            'city': profile.city,
            'district': profile.district,
            'house_number': profile.house_number,
            'street': profile.street,
            'cep': profile.cep,
        }

        # form = CheckoutForm(initial=initial_data)

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        checkoutForm = CheckoutForm(initial=initial_data)
        date = timezone.now()
        prazo_entrega = date + timedelta(days=15)
        checkout_url = reverse('page_checkout')  # Ou a URL que você usa
        return render(request,'checkout.html', {'checkoutForm': checkoutForm,
                                                'prazo_entrega':prazo_entrega, 
                                                'checkout_url': checkout_url, 
                                                'friend_requests':friend_requests,
                                                'profile': profile})

def pix_payment(request):
    if request.user.is_authenticated:
        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        return render(request,"pix_payment", {'friend_requests':friend_requests,})
def boleto_payment(request):
    if request.user.is_authenticated:
        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        return render(request,"boleto_payment", {'friend_requests':friend_requests,})
def card_payment(request):
    if request.user.is_authenticated:
        user_logged = request.user

        # Buscar solicitações de amizade
        friend_requests =  FriendRequest.objects.filter(to_user=user_logged, accepted=False, rejected=False)
        return render(request,"card_payment", {'friend_requests':friend_requests,})

# Essa função redireciona o usuario que esta na pagina de checkout para a pagina de meio de pagamento 
def finish_purchase(request):
    user_logged = get_object_or_404(UserProfile, user=request.user)  # Usuário logado
    checkoutForm = CheckoutForm(instance=user_logged)
    print("checkoutForm: ", checkoutForm)
    
    payment_method = request.POST.get("payment") # valor pego pelo name da tag (name="payment")
    total_value = request.POST.get("total-value") # valor pego pelo name da tag (name="total-value")
    order_number = request.POST.get("hidden_order_number") # valor pego pelo name da tag (name="hidden_order_number")
    
    
    if not payment_method:
        messages.error(request, "Selecione um meio de pagamento.")
        return redirect('page_checkout')
    
    
    if request.method == 'POST':   
        print("TESTE",payment_method)
        print("TESTE VALOR TOTAL",total_value)
        print("TESTE request.POST:", request.POST) # Verifica o que esta sendo enviado na requisição  
        print("order_number: ", order_number)
        
        if order_number:
            try:
                response = requests.get(f'http://localhost:8080/api/v1/order/total-price/{order_number}/')
                print("response: ", response)
                if response.status_code == 200:
                    api_data = response.json()
                    total_price = api_data.get('total_price')
                else:
                    messages.error(request,"Erro ao obter o preço total do pedido")
                    return redirect('page_checkout')
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Erro ao se comunicar com a API: {str(e)}")
                return redirect('page_checkout')
            
        
        if payment_method == "pix":                        
            return render(request,"pix_payment.html",{'checkoutForm':checkoutForm, "total_value":total_value, "order_number":order_number, "total_price":total_price,})
        elif payment_method == "boleto":
            return render(request,"boleto_payment.html",{'checkoutForm':checkoutForm, "total_value":total_value, "order_number":order_number, "total_price":total_price,})
        elif payment_method == "cartao":
            return render(request,"card_payment.html",{'checkoutForm':checkoutForm,"total_value":total_value, "order_number":order_number, "total_price":total_price,})
        else:
            messages.error(request,"Selecione um meio de pagamento.")
            return redirect('page_checkout')
        
        
    else:
        messages.error(request,"Selecione um meio de pagamento.")
        return redirect('page_checkout')
    
    
# def generate_barcode(request, order_number):
#     print("Esse é o barcode_value: ",order_number)
    
#     # zxing_generator = zxing.BarCodeGenerator()
#     # zxing_generator = zxing.BarCode(uri="/static/barcodes")

#     image_path = "/tmp/barcode.png"
#     zxing_generator.encode(order_number, "code128", image_path)
    
#     with open(image_path, 'rb') as f:
#         return HttpResponse(f.read(), content_type="image/png")
    
    
    
    
    
    # barcode_format = barcode.get_barcode_class('Code128')
    # # barcode_format = Code128
    # barcode_instance = barcode_format(barcode_value, writer=ImageWriter())
    
    # # barcode_instance = Code128(barcode_value, writer=ImageWriter())
    
    # # barcode_instance.writer.set_options({'text': ''})

    # buffer = BytesIO()
    # barcode_instance.write(buffer)
    # buffer.seek(0)
    
    # print("Código de barras gerado com sucesso.")

    # return HttpResponse(buffer, content_type="image/png")
            






















        # # Ao tentar validar o formulário de checkout, o django mostrava que não esta sendo enviada uma resposta http valida
        # if checkoutForm.is_valid():
        #     if payment_method == "pix":            
        #         checkoutForm.save()
        #         return render(request,"pix_payment.html",{'checkoutForm':checkoutForm})
        #     elif payment_method == "boleto":
        #         checkoutForm.save()
        #         return render(request,"boleto_payment.html",{'checkoutForm':checkoutForm})
        #     elif payment_method == "cartao":
        #         checkoutForm.save()
        #         return render(request,"card_payment.html",{'checkoutForm':checkoutForm})
        #     else:
        #         messages.error(request,"Selecione um meio de pagamento.")
        #         return redirect('page_checkout')







# def send_friend_request(request,id):
#     # friend_request = get_object_or_404(FriendRequest, id=id)
#     user_logged = request.user # usuario logado
#     user_profile = get_object_or_404(UserProfile, id=id)  # Usuário visitado
#     user_logged.send_friend_request(user_profile)
#     messages.success(request, f"AA Solicitação para {user_profile.user.username} enviada com sucesso.")
#     print("FRIEND REQUEST")
#     return redirect('profile_view', id=user_profile.id)




# def remove_friend(request, id):
#     user_profile_to_remove = get_object_or_404(UserProfile, id=id)
#     user_logged = request.user  # Usuário logado
#     user_logged.remove_friend(user_profile_to_remove)
#     friend_request_solicitation = FriendRequest.objects.filter(from_user=user_logged, to_user=user_profile_to_remove).exists()
#     if friend_request_solicitation.exists():
#         friend_request_solicitation.delete()
#         print("DELETE SOLICITATION UNFOLLOW")
#     # return redirect('profile_view', id=user_profile_to_remove.to_user.id)
#     # return render(request, 'profile_view.html', id=user_profile_to_remove.to_user.id, {"friend_request_solicitation":friend_request_solicitation})
#     return render(request, 'profile_view.html', {'id': user_profile_to_remove.to_user.id, 'friend_request_solicitation': friend_request_solicitation})


                

            # if 'accept_friend_request' in request.POST:
            #     user_logged_profile = get_object_or_404(UserProfile, user=request.user)
            #     user_logged_profile.accept_friend_request(user_profile_instance)
            #     messages.success(request, f"Você aceitou a solicitação de amizade de {user_profile_instance.user.username}")
            #     print("ACCEPT")
            #     return redirect('profile_view', id=user_profile.id)


            # if 'reject_request' in request.POST:
            #     user_logged_profile = get_object_or_404(UserProfile, user=request.user)
            #     user_logged_profile.remove_friend(user_profile_instance)
            #     # messages.success(request, f"Você recusou a solicitação de amizade de {user_profile_instance.user.username}")
            #     # print("REJECT")
            #     # return render(request,'profile_view.html', {'friend_request_solicitation':friend_request_solicitation})
                




    # new_size = size[0]
    
    # if original_width > original_height:
    #     new_width = size[0]
    #     new_height = int((new_width / original_width) * original_height)
    #     img = img.resize((new_width, new_height), Image.LANCZOS) # Image.LANCZOS é o método adequado para redimensionamento com alta qualidade
        
    #     top = (new_height - size[1]) // 2
    #     left = (new_width - size[0]) // 2
    #     img = img.crop((left, top, left + size[0], top + size[0]))
    # else:
    #     new_height = size[1]
    #     new_width = int((new_height / original_height) * original_width)
    #     img = img.resize((new_width, new_height), Image.LANCZOS) # Image.LANCZOS é o método adequado para redimensionamento com alta qualidade
        
    #     top = (new_height - size[1]) // 2
    #     left = (new_width - size[0]) // 2
    #     img = img.crop((left, top, left + size[0], top + size[0]))













# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Carrinho de {self.user.username}"
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, related_name='cart_items', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def __str__(self):
#         return f"{self.quantity} x {self.book.title}"
    
#     def total_price(self):
#         return self.book.value * self.quantity
        
        
        
        
        
        
        
        
        
        
        



        
        # Remover avaliações duplicadas por livro ( Não da pra fazer com set pois se não vai ser perdido as propriedades de busca )
        # unique_ratings = []
        # unique_ratings_index = []   
        # seen_books = set()
        # for i,rating in enumerate(ratings):
        #     if rating.book not in seen_books: # Se o livro não existe em seen_books (livros vistos)
        #         unique_ratings.append(rating)
        #         seen_books.add(rating.book) # adiciona a livros vistos impedindo que ocorra repetições de itens
        #         unique_ratings_index.append(i)
        #     if len(unique_ratings) == 5:
        #         break
        
        
        
        
        
        
        
        
        
        
        
        

# def sobre(request):
#     return HttpResponse("Teste Sobre")
    
    
    
## MODELO ANTIGO SEM OS COMENTÁRIOS:
## Só vai acessar os detalhes do livro se estiver autenticado
# def book_detail(request, id):
#     if request.user.is_authenticated:
#         book = Book.objects.get(id =id)
#         return render(request, 'book.html', {'book':book})  # {'book': book} é um dicionário sendo passado para o contexto da página que será renderizada.
#     else:
#         messages.error(request, 'Você precisa estar logado!')
#         return redirect('home')
    
    
    
    
    
    