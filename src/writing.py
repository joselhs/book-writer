from utils import BaseEventChain


class WriterChain(BaseEventChain):
    
    PROMPT = """
    Eres un escritor de novelas. La novela está descrita por una lista de eventos.
    Ya has escrito la novela hasta el último evento.
    Tu trabajo es generar los parrafos de la novela sobre un nuevo evento.
    Se te provee el título de la novela, la trama de la novela, la descripción del personaje principal y la trama del capítulo actual.
    Asegurate que los párrafos son consistentes con la trama de la novela.
    Además, se te provee con una lista de eventos sobre los que ya has escrito.
    Los párrafos deben ser consistentes con el género de la novela.
    Los párrafos deben ser consistentes con el estilo del autor.

    Género: {genre}
    Autor: {author}
    Título: {title}
    Descripción del personaje principal: {profile}

    Trama de la novela: {plot}
    Eventos previos:
    {previous_events}

    Resumen del capítulo actual: {summary}

    Párrafos previos: 
    {previous_paragraphs}

    Nuevo evento sobre el que tienes que escribir:
    {current_event}

    Párrafos de la novela describiendo ese evento:"""


    def run(self, genre, author, title, profile, plot, previous_events,
            summary, previous_paragraphs, current_event):
          
          previous_events = '\n'.join(previous_events)

          return self.chain.predict(genre=genre, 
                                   author=author, 
                                   title=title, 
                                   profile=profile, 
                                   plot=plot, 
                                   previous_events=previous_events, 
                                   summary=summary, 
                                   previous_paragraphs=previous_paragraphs, 
                                   current_event=current_event)
    

def write_book(genre, author, title, profile, plot, summaries_dict, events_dict):
    writer_chain = WriterChain()
    previous_events = []
    book = {}
    paragraphs = ''

    for chapter, events_list in events_dict.items():
            
        book[chapter] = []

        for event in events_list:

            paragraphs = writer_chain.run(
                genre=genre,
                author=author,
                title=title,
                profile=profile,
                plot=plot,
                previous_events=previous_events,
                summary=summaries_dict[chapter],
                previous_paragraphs=paragraphs,
                current_event=event
            )

            previous_events.append(event)
            book[chapter].append(paragraphs)

    return book
