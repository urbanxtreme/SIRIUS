from database import add_media_from_directory

# Insert images
add_media_from_directory('images/galaxies', 'cosmology', 'image')
add_media_from_directory('images/nebulas', 'exoplanets', 'image')
add_media_from_directory('images/stars', 'galaxies', 'image')
add_media_from_directory('images/stars', 'nebulas', 'image')
add_media_from_directory('images/stars', 'solar system', 'image')
add_media_from_directory('images/stars', 'stars', 'image')
add_media_from_directory('images/stars', 'webb mission', 'image')

# Insert audio
add_media_from_directory('audio/anxiety', 'anxiety', 'audio')
add_media_from_directory('audio/desperate', 'desperate', 'audio')
add_media_from_directory('audio/enjoy', 'enjoy', 'audio')
add_media_from_directory('audio/loneliness', 'loneliness', 'audio')
add_media_from_directory('audio/optimistic', 'optimistic', 'audio')
add_media_from_directory('audio/romantic', 'romantic', 'audio')