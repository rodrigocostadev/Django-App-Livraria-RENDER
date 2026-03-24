from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to="users", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # cpf = models.IntegerField(unique=True, null=False)
    # cpf = models.IntegerField(null=False)
    cpf = models.CharField(max_length=11,null=False)   
    
    state = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)
    district = models.CharField(max_length=50,null=True)
    house_number = models.IntegerField(null=True)
    street = models.CharField(max_length=50,null=True)
    cep = models.IntegerField(null=True)
    
    # friends = models.ManyToManyField('self', blank=True, symmetrical=False)  # Seguindo
    
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by') # seguidores
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='follows') # seguindo
    
    # friends: O campo ManyToManyField permite que você crie uma relação de amizade entre os usuários. 
    # Usamos 'self' para que a relação seja com a mesma tabela, ou seja, um usuário com outro usuário.
    
    # O argumento symmetrical=False é importante porque a amizade não é automaticamente bidirecional 
    # (ou seja, se A é amigo de B, B não será amigo automaticamente de A sem uma ação explícita). 
    # O symmetrical=False permite que você trate a amizade de forma manual.
    
    def send_friend_request(self, to_user_profile):
        # Previne que o usuário envie uma solicitação para si mesmo
        # if self != to_user_profile:
        FriendRequest.objects.create(from_user=self.user, to_user=to_user_profile.user)

            
    def accept_friend_request(self,from_user_profile):
        request = FriendRequest.objects.get(from_user=from_user_profile.user, to_user=self.user) # Encontra a solicitação de amizade
        request.accepted = True # Marca a solicitação como aceita
        request.save()
        self.followers.add(from_user_profile) # Adiciona o nome do usuario a minha lista de seguidores
        from_user_profile.following.add(self) # Adiciona o meu usuario na lista de seguidores do outro usuario
        # from_user_profile.friends.add(self) # maneira antiga
        
        request.delete() # Remove a solicitação de amizade aceita
        
        
        
    # def reject_friend_request(self, from_user_profile):
    #     request = FriendRequest.objects.get(from_user=from_user_profile.user, to_user=self.user) # Encontra a solicitação de amizade
    #     request.reject = True # marca a solicitação como rejeitada
    #     request.save()        
    #     request.delete() # Remove a solicitação de amizade aceita
        
        
    def remove_follower(self, from_user_profile): # Remove seguidores
        if from_user_profile in self.followers.all():
            self.followers.remove(from_user_profile)
            from_user_profile.followers.remove(self)            
            from_user_profile.following.remove(self)
            
            
    def unfollow(self,from_user_profile):
        self.following.remove(from_user_profile)
        from_user_profile.followers.remove(self)





class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_requests') # Usuario que mandou o convite
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests') # Usuario que recebe o convite
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    # from_user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    # to_user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_friend_requests')
    
    def __str__(self):
        return f"Solicitação de {self.from_user.username} para {self.to_user.username}"
    
    @property # Permite usar o método from_user_image sem o uso dos parenteses no final, como se fosse uma propriedade
    def from_user_image(self):
        # Acessa a imagem do usuário que enviou a solicitação de amizade.
        return self.from_user.userprofile.user_image 



class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500,null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=30)
    value = models.FloatField()
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images")
    media_rating = models.DecimalField(default=0, max_digits=3, decimal_places=1, )
    tags = TaggableManager() # tags é o campo onde você pode adicionar múltiplas tags (como "Ficção", "Tecnologia", etc.)
    
    def __str__(self):
        return(f'{self.title} - {self.value}')
    
    
    
    
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300) # Limita o numero de caracteres a serem armazenados no banco de dados
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentário de {self.user.username} para {self.book.title}"
    
    
    
class RatinStar(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_review = models.IntegerField(default=0)
    genre = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # media_rating = models.DecimalField(default=0,max_digits=3,decimal_places=1,)     COLOCAR MEDIA DE RATING
    # rating = models.IntegerField()    
    
    rating = models.DecimalField(
        max_digits=3,    # Número total de dígitos (antes e depois do ponto decimal)  "numero ponto numero"
        decimal_places=1, # Número de casas decimais após o ponto
        )
    
    def __str__(self):
        return f"Avaliação de {self.user} para o livro {self.book.title} ({self.book.genre}), nota: {self.rating} / numero de avaliações: {self.n_review}"
    
    
    
    
# class Checkout(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)    
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, default="pendente")
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     address = models.TextField()
    
    
#     def __str__(self):
#         return f"Compra realizada por {self.user.username} em {self.created_at}"



# class CheckoutItem(models.Model):
#     checkout = models.ForeignKey(Checkout,related_name='items', on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10,decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.book.title} para {self.checkout.user.username}"



