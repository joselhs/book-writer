from utils import BaseStructureChain, ChatOpenAI


class TitleChain(BaseStructureChain):

    PROMPT = """
    Tu trabajo es generar el título para una novela sobre la siguiente temática y personaje principal.
    Devuelve solo el título y solo el título!!
    El título debe ser consistente con el género de la novela.
    El título debe ser consistente con el estilo del autor.

    Temática: {subject}
    Género: {genre}
    Author: {author}

    Perfil del personaje principal: {profile}
    Título"""

    def run(self, subject, genre, author, profile):
        return self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile
        )
    

class PlotChain(BaseStructureChain):

    PROMPT = """
    Tu trabajo es generar la trama para una novela. Devuelve el argumento y solo el agrumento!
    Describe la trama completa de la historia y no dudes en añadir nuevos personajes si lo necesitas para hacerla convincente.
    Se te provee la siguiente temática, el título de la novela y el perfil del personaje principal.
    Asegurate de que el personaje principal es el centro de la historia.
    La trama debe ser consistente con el género de la novela.
    La trama debe ser consistente con el estilo del autor.

    Considera los siguientes atributos para escribir una historia fascinante:
    {features}

    Temática: {subject}
    Género: {genre}
    Autor: {author}

    Título: {title}
    Perfil del personaje principal: {profile}

    Trama:"""

    HELPER_PROMPT = """
    Genera una lista de atributos que caracterizan a una historia fascinante.

    Lista de atributos:"""

    def run(self, subject, genre, author, profile, title):
        features = ChatOpenAI().predict(self.HELPER_PROMPT)

        plot = self.chain.predict(
            features=features,
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title
        )
        return plot



class ChaptersChain(BaseStructureChain):

    PROMPT = """
    Tu trabajo es generar una lista de capítulos.
    Sólo la lista, nada más!

    Se te provee con el título, la trama y el personaje principal de una novela.
    Genera una lista de capítulos describiendo la trama de esa novela.
    Asegurate que los capítulos son consistentes con la trama.
    Los capítulos deben ser consistentes con el género de la novela.
    Los capítulos deben ser consistentes con el estilo del autor.

    Sigue este plantilla:

    Prólogo: [descripción del prólogo]
    Capítulo 1: [descripción del capítulo]
    ...
    Epílogo: [descripción del epílogo]

    Asegurate de que el capítulo está seguido de `:` y su descripción. Por ejemplo: `Capítulo 1: [descripción del capítulo]`

    Temática: {subject}
    Género: {genre}
    Autor: {author}

    Título: {title}
    Perfil del personaje principal: {profile}

    Trama: {plot}

    Devuelve la lista de capítulos y solo la lista de capítulos:"""

    def run(self, subject, genre, author, title, profile, plot):
        response = self.chain.predict(subject=subject, 
                                      genre=genre, 
                                      author=author, 
                                      title=title, 
                                      profile=profile, 
                                      plot=plot)
        return self.parse(response)

    
    def parse(self, response):
        chapter_list = response.strip().split('\n')
        chapter_list = [chapter for chapter in chapter_list if ':' in chapter]

        chapter_dict = dict([
            chapter.strip().split(':')
            for chapter in chapter_list
        ])

        return chapter_dict
    

def get_structure(subject, genre, author, profile):
    title_chain = TitleChain()
    plot_chain = PlotChain()
    chapters_chain = ChaptersChain()

    title = title_chain.run(subject=subject, genre=genre, author=author, profile=profile)
    plot = plot_chain.run(subject=subject, genre=genre, author=author, profile=profile, title=title)
    chapter_dict = chapters_chain.run(subject=subject, genre=genre, author=author, profile=profile, title=title, plot=plot)

    return title, plot, chapter_dict