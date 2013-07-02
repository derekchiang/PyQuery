# PyQuery

PyQuery is a backend-agnostic database query framework.  It exposes an API similar to SQLAlchemy, but makes it easy to write drivers for NoSQL databases like Cassandra, MongoDB, etc.

## Status

Unstable.  Work in progress.

## Rationale

Many applications eventually grow to a point where they need to support multiple databases.  However, different databases expose very different APIs, sometimes making it necessary to rewrite business logic.

As an example, let's say you are developing a video game and you have two tables: leagues and players.  A player belongs to a league.

Using an SQL database, to query a player, you would do something like this:

'''python

def get_players_of_league(player_id):
	query(models.Player).filter(id = player_id).first()

'''

Now let's say you want to have a Cassandra backend.  Since Cassandra doesn't have native support for relationships, you want to have a `league` table (or *column family* in Cassandra's parlance) containing JSON-serialized players.  Now you will have to write a separate driver containing code like:

'''python

def get_players_of_league(player_id):
	leagues = query(models.League).all()
	for league in leagues:
		players = deserialize(league.players)
		for player in players:
			if player.id == player_id:
				return player
	return None

'''

The point here is that, because of the difference in the underlying DB models, you end up duplicating your business logic (namely, querying a player by id) in different DB drivers.  This is very bad.

## PyQuery to the Rescue

Continuing with the previous example, we now use the awesome PyQuery:

'''python

def get_players_of_league(player_id):
	Query(models.Player).filter(EqualTo('id', player_id)).first()

'''

It's almose identical to the SQL code.  However, this code will continue to work if you decide to use a NoSQL database.  All you need to do is to define a relation in your NoSQL driver, like this:

'''python

class LeagueHasManyPlayers(OneToMany):
    def query(attribute):
        leagues = query(models.League).all()
		for league in leagues:
			players = deserialize(league.players)
			for player in players:
				if attribute.match(player):
					yield player
		return None

relations.add_relation(LeagueHasManyPlayers(models.League, models.Player))

'''

Having this relationship defined, it won't matter if the calling code is querying for players but you don't have a player table.  PyQuery will make sure that when players are being queryed, it will use the logic defined in the relationships to find the right data.

As a result, you now have your business logic defined in one place and one place only.  DB drivers will only need to define the query logic between the underlying DB tables.  A clear separation between your business logic and the DB logic is thus established.