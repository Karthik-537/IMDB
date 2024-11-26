from .models import Director, Actor, Movie, Cast, Rating
from django.db.models import Avg
from django.db.models import Count
def get_all_actor_objects_acted_in_given_movies(movies):
    actors = Cast.objects.filter(movie__in=movies).values_list('actor', flat=True).distinct()
    distinct_actors = Actor.objects.filter(actor_id__in=actors)
    return distinct_actors
def update_director_for_given_movie(movie_obj, director_obj):
    movie_obj.director=director_obj
    movie_obj.save()
    return movie_obj.director
def get_all_rating_objects_for_given_movies(movie_objs):
    ratings=Rating.objects.filter(movie__in=movie_objs)
    return ratings
def get_movies_released_in_summer_in_given_years():
    m=Movie.objects.filter(release_date__month__in=[5,6,7],release_date__year__range=(2020,2024))
    return m
def get_movie_names_with_actor_name_ending_with_smith():
    a=Actor.objects.filter(name__iendswith='B')
    m=Cast.objects.filter(actor__in=a).values('movie__name').distinct()
    return m
def get_movie_names_with_ratings_in_given_range():
    r=Rating.objects.filter(rating_five_count__gte=5,rating_five_count__lte=15).values_list('movie__name',flat=True).distinct()
    return r
def get_movie_names_with_ratings_above_given_minimum():
    m=Movie.objects.filter(release_date__year__gt=2000)
    r=Rating.objects.filter(movie__in=m,rating_five_count__gt=5,rating_four_count__gt=2,rating_three_count__gt=2,rating_two_count__gt=2,rating_one_count__gt=1).values_list('movie__name',flat=True)
    return r
def get_movie_directors_in_given_year():
    r=Movie.objects.filter(release_date__year=2024).values_list('director__name',flat=True)
    return r
def get_actor_names_debuted_in_21st_century():
    c=Cast.objects.filter(is_debut_movie=True).values_list('actor__name',flat=True)
    return c
def get_average_box_office_collections():
    b=Movie.objects.aggregate(Avg('box_office_collection_in_crores'))
    return b
def get_movies_with_actor_counts():
    movies = Movie.objects.annotate(actors_count=Count('cast__actor', distinct=True))
    return [{movie.name:movie.actors_count} for movie in movies]
def get_role_frequency():
    roles_with_actor_counts = (
        Cast.objects.values('role')
        .annotate(actor_count=Count('actor', distinct=True))
        .order_by('role')
    )
    result = {entry['role']: entry['actor_count'] for entry in roles_with_actor_counts}
    return result
def get_role_frequency_in_order():
    m=Movie.objects.all().order_by('-release_date').first()
    roles_with_actor_counts = (
        Cast.objects.filter(movie=m).values('role')
        .annotate(actor_count=Count('actor', distinct=True))
    )
    result=[]
    for entry in roles_with_actor_counts:
        result.append(entry)
    return result
def get_all_rating_objects_for_given_movies():
    m1 = Movie.objects.get(name='Bahubali')
    m2 = Movie.objects.get(name='RRR')
    movies = [m1, m2]
    R=Rating.objects.filter(movie__in=movies)
    return [r for r in R]
def get_movies_by_given_movie_names(movie_names):
    movie_details = []
    movies = Movie.objects.filter(name__in=movie_names)
    for movie in movies:
        cast_details = []
        cast_objects = Cast.objects.filter(movie=movie)
        for cast in cast_objects:
            cast_details.append({
                "actor": {
                    "name": cast.actor.name,
                    "actor_id": cast.actor.actor_id
                },
                "role": cast.role,
                "is_debut_movie": cast.is_debut_movie
            })
        rating_stats = Rating.objects.filter(movie=movie).aggregate(
            average_rating=Avg('rating_five_count'),
            total_number_of_ratings=Count('id')
        )
        movie_data = {
            "movie_id": movie.movie_id,
            "name": movie.name,
            "cast": cast_details,
            "box_office_collection_in_crores": movie.box_office_collection_in_crores,
            "release_date": movie.release_date,
            "director_name": movie.director.name,
            "average_rating": rating_stats.get('average_rating', 0),
            "total_number_of_ratings": rating_stats.get('total_number_of_ratings', 0)
        }
        movie_details.append(movie_data)
    return movie_details
def get_all_actor_objects_acted_in_given_movies():
    m1=Movie.objects.get(name='Bahubali')
    m2=Movie.objects.get(name='RRR')
    l=[m1,m2]
    m=Actor.objects.filter(cast__movie__in=l).distinct()
    return m
def reset_ratings_for_movies_in_this_year():
    R=Rating.objects.filter(movie__release_date__year=2024)
    for r in R:
        r.rating_one_count=0
        r.rating_two_count=0
        r.rating_three_count=0
        r.rating_four_count=0
        r.rating_five_count=0
    return R
def get_movie_directors_in_given_year():
    d=Director.objects.filter(movie__release_date__year=2024).values_list('name',flat=True)
    return d
def get_director_names_containing_big_as_well_as_movie_in_may():
    d=Director.objects.filter(movie__name__contains='Ka',movie__release_date__month=6).values_list('name',flat=True)
    return d
def get_movies_with_distinct_actors_count():
    movies = Movie.objects.annotate(actors_count=Count('cast__actor', distinct=True))
    return [movie.name for movie in movies]
def get_no_of_movies_and_distinct_roles_for_each_actor():
    A=Actor.objects.annotate(movies_count=Count('cast__movie'),roles_count=Count('cast__role',distinct=True))
    return [a.roles_count for a in A]
def get_movies_with_atleast_forty_actors():
    m=Movie.objects.annotate(actors_count=Count('cast__actor',distinct=True)).filter(actors_count__gt=1)
    return m
def get_average_no_of_actors_for_all_movies():
    A=Movie.objects.annotate(average=Count('cast__actor',distinct=True))
    result=A.aggregate(a=Avg('average'))
    return round(result['a'],3) if result else 0
def get_average_rating_of_movie():
    m=Movie.objects.get(name='RRR')
    a=Rating.objects.filter(movie=m).aggregate(average=Avg('rating_five_count'))
    return a['average']