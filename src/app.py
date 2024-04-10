from dotenv import load_dotenv

load_dotenv()

from characters import MainCharacterChain
from structure import get_structure
from events import get_events
from writing import write_book
from publishing import DocWriter

subject = 'Artificial Dreams'
author = 'Brandon Sanderson'
genre = "Science Fiction"

main_character_chain = MainCharacterChain()
profile = main_character_chain.run('Profile.pdf')
doc_writer = DocWriter()

title, plot, chapter_dict = get_structure(subject=subject, genre=genre, author=author, profile=profile)
summaries_dict, events_dict = get_events(subject=subject, genre=genre, author=author, 
                                         profile=profile, title=title, plot=plot, chapter_dict=chapter_dict)

book = write_book(genre=genre, author=author, title=title, profile=profile, plot=plot, 
                  summaries_dict=summaries_dict, events_dict=events_dict)

doc_writer.write_doc(book=book, chapter_dict=chapter_dict, title=title)


