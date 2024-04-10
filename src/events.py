from utils import BaseEventChain, ChatOpenAI


class ChapterPlotChain(BaseEventChain):

    HELPER_PROMPT = """
    Genera una lista de características que caracterizan a una historia fascinante.
    Lista de características:"""

    PROMPT = """
    Eres un Escritor y tu trabajo es generar la trama para un capitulo, y solo un capítulo, de una novela.
    Se te provee el título, la trama principal y el personaje principal de la novela.
    Además, se te provee con la trama de los capitulos anteriores y el esquema de la novela.
    Asegurate de generar una trama que describe de forma precisa la historia del capítulo.
    Cada capítulo tiene que tener su propio arco, pero debe ser consistente con los otros capítulos y la historia global de la novela.
    El resumen debe ser consistente con el género de la novela.
    El resumen debe ser consistente con el estilo del autor.

    Considera los siguientes atributos para escribir una historia fascinante:
    {features}

    Temática: {subject}
    Género: {genre}
    Autor: {author}

    Título: {title}
    Perfil del personaje principal: {profile}

    Trama de la novela: 
    {plot}

    Esquema: {outline}

    Trama de los capitulos:
    {summaries}

    Devuelve la trama y solo la trama para el capítulo.
    Trama del capítulo: {chapter}"""

    
    def run(self, subject, genre, author, profile, title, 
            plot, summaries_dict, chapter_dict, chapter):
        
        features = ChatOpenAI().predict(self.HELPER_PROMPT)

        outline = '\n'.join([
            '{} - {}'.format(chapter, description)
            for chapter, description in chapter_dict.items()
        ])

        summaries = '\n\n'.join([
            'Plot of {}: {}'.format(chapter, summary)
            for chapter, summary in summaries_dict.items()
        ])

        return self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            features=features,
            outline=outline,
            summaries=summaries,
            chapter=chapter
        )




class EventsChain(BaseEventChain):
    
    PROMPT = """
    Eres un escritor y tu trabajo es generar una lista detallada de los eventos que suceden en el capítulo actual de una novela.
    Esos eventos describen la trama del capítulo y las acciones de los diferentes personajes en un orden cronológico.
    Se te provee el título, la trama principal de la novela, el personaje principal y un resumen de ese capítulo.
    Además, se te provee con una lista de eventos que sucedieron en los capítulos anteriores.
    La lista de eventos debe ser consistente con el género de la novela.
    La lista de eventos debe ser consistente con el estilo del autor.

    Cada elemento de esa lista debe devolverse en una línea diferente. Sigue la siguiente plantilla:

    Evento 1
    Evento 2
    ...
    Evento Final 


    Temática: {subject}
    Género: {genre}
    Autor: {author}

    Título: {title}
    Perfil del personaje principal: {profile}

    Trama de la novela: {plot}
    
    Eventos destacados de los capítulos anteriores: {previous_events}

    Resumen del capítulo actual: 
    {summary}
    
    Devuelve los eventos y solo los eventos!!
    Lista de eventos para el capítulo:"""


    def run(self, subject, genre, author, profile, title, plot, summary, events_dict):
        previous_events = ''
        for chapter, events in events_dict.items():
            previous_events += '\n' + chapter
            for event in events:
                previous_events += '\n' + event
        
        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            summary=summary,
            previous_events=previous_events
        )

        return self.parse(response)
    

    def parse(self, response):
        event_list = response.strip().split('\n')
        event_list = [
            event.strip() for event in event_list if event.strip()
        ]
        return event_list


def get_events(subject, genre, author, profile, title, plot, chapter_dict):
    chapter_plot_chain = ChapterPlotChain()
    events_chain = EventsChain()
    summaries_dict = {}
    events_dict = {}

    for chapter, _ in chapter_dict.items():

        summaries_dict[chapter] = chapter_plot_chain.run(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            summaries_dict=summaries_dict,
            chapter_dict=chapter_dict,
            chapter=chapter
        )

        events_dict[chapter] = events_chain.run(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            summary=summaries_dict[chapter],
            events_dict=events_dict
        )
    return summaries_dict, events_dict