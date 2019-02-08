# Background

This are the beginning of all great things that can happen in my life. Pesbuk are going to revolutionize the way people interact with internet. The one and only reall competitor to facebook. Pesbuk ini bossqu, bukan kaleng-kaleng =D

# Project pesbuk

To run this code simply clone/download this project into your machine then navigate to the directory of this folder where Dockerfile sit then run the command.

  	docker-compose build && docker-compose up
  	
After it you execute command above then can take a look into api docs bellow to start using my pesbuk api.

# Api documentations

Related api to run this project has been documented awesomely in link bellow (Thanks to Mr. Postman):

    https://documenter.getpostman.com/view/236547/RztppnZw
    
# DB schema 

Database schema and all of it greatness can be found in activity.models.py or check bellow:
    
    class User(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'


    class Activity(models.Model):
        actor_id = models.IntegerField(null=False)
        verb = models.CharField(max_length=256, null=False)
        object = models.CharField(max_length=256, null=True)
        target_id = models.IntegerField(null=True)
        creation_time = models.DateTimeField(auto_now_add=True)
        modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activity_feed'
        unique_together = ('actor_id', 'verb', 'object', 'target_id')


    class FriendShip(models.Model):
        actor_id = models.IntegerField(null=False, unique=True)
        friend_ids = models.TextField(null=False)
        creation_time = models.DateTimeField(auto_now_add=True)
        modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'friend_status'

# Others
 
 Thank you for this opportunity dear great people who willing to take a look into this project of mine. I chose to use django because I have been using django much more frequently in recent times, I would love to re-explore to build this api with Flask ,since this project are suppose to be simple and small in size, but taking time into considerations I would not be able to complete this project in time, since I might have to re-look into flask docs and stuff and it will consumer some additional time. So django it is.
 
    Django, D-J-A-N-G-O, the D is silent

Thank you to Bapak Eric Pierce, and Pak Andriano Winarta for this interview opportunity. And thank you to Dear Jesus for everything thy have given me in this life. God bless you all. Cheers!

    28 Do you not know? Have you not heard? The LORD is the everlasting God, the Creator of the ends of the earth. He will not grow tired or weary, and his understanding no one can fathom. 
    29 He gives strength to the weary and increases the power of the weak. 
    30 Even youths grow tired and weary, and young men stumble and fall; 
    31 but those who hope in the LORD will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.
    
    Isaiah 40:28-31 