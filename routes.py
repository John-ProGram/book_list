from flask import Blueprint, request, jsonify
from database.database_manager import DatabaseManager
from datetime import datetime

# Com Blueprints, eu posso mover essas rotas para arquivos separados e depois registrar tudo no seu app principal
routes_bp = Blueprint("routes_bp", __name__)
dbm = DatabaseManager

@routes_bp.route("/books", methods=["GET"])
def get_books():
    sql = "SELECT * FROM books"
    result = dbm.execute_sql_str(sql, query=True)
    books = [
        {
            "isbn": row["isbn"],
            "book_name": row["book_name"],
            "publisher": row["publisher"],
            "published_date": row["published_date"].isoformat(),
            "author": row["author"]
        }
        for row in result
    ]
    return jsonify(books), 200


@routes_bp.route("/books/<string:isbn>", methods=["GET"])
def get_books_by_isbn(isbn):
    sql = "SELECT * FROM books WHERE isbn = :isbn"
    result = dbm.execute_sql_str(sql, query=True)
    if result:
        row = result[0]
        return jsonify({
            "isbn": row["isbn"],
            "book_name": row["book_name"],
            "publisher": row["publisher"],
            "published_date": row["published_date"].isoformat(),
            "author": row["author"]
        }), 200
    return jsonify({"erro": "Livro não encontrado"}), 404


@routes_bp.route("/books/<string:isbn>", methods=["POST"])
def post_books():
    livro_dados = request.get_json()
    print(livro_dados)
    published_date_str = livro_dados.get("published_date", "")
    try:
        book_name = livro_dados["book_name"]
        publisher = livro_dados["publisher"]
        published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
        author = livro_dados["author"]
        isbn = livro_dados["isbn"]
        livro = Book(
            book_name=book_name,
            publisher=publisher,
            published_date=published_date,
            author=author,
            isbn=isbn
        )
        db.session.add(livro)
        db.session.commit()
        return jsonify(msg="Livro adicionado com sucesso"), 201
    except KeyError as error:
        return jsonify({"error": "Chave faltante: " + str(error)}), 400
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@routes_bp.route("/books/<string:isbn>", methods=["PUT"])
def update_book(isbn):
    livro_dados = request.get_json()
    print(livro_dados)
    published_date_str = livro_dados.get("published_date", "")
    try:
        book_name = livro_dados["book_name"]
        publisher = livro_dados["publisher"]
        published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
        author = livro_dados["author"]
        isbn = livro_dados["isbn"]
        livro = Book(
            book_name=book_name,
            publisher=publisher,
            published_date=published_date,
            author=author,
            isbn=isbn
        )
        db.session.commit()
        return jsonify(msg="Livro alterado com sucesso"), 201
    except KeyError as error:
        return jsonify({"error": "Chave faltante: " + str(error)}), 400
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@routes_bp.route("/books/<string:isbn>", methods=["DELETE"])
def delete_book(isbn):
    livro = Book.query.filter_by(isbn=isbn).first()

    if not livro:
        return jsonify(msg="Livro não encontrado"), 404

    db.session.delete(livro)
    db.session.commit()
    return jsonify(msg="Livro deletado com sucesso"), 404


@routes_bp.route("/authors", methods=["PATCH"])
def patch_books(isbn):
    livro_dados = request.get_json()
    livro = Book.query.filter_by(isbn=isbn).first()

    if not livro:
        return jsonify(msg="Livro não encontrado"), 404

    campos_validos = ["book_name", "publisher", "published_date", "author", "isbn"]

    try:
        for campo, valor in livro_dados.items():
            if campo in campos_validos:
                if campo == "published_date":
                    valor = datetime.strptime(valor, "%Y-%m-%d").date()
                setattr(livro, campo, valor)

        db.session.commit()
        return jsonify(msg="Livro atualizado com sucesso"), 200
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    

@routes_bp.route("/authors", methods=["GET"])
def get_authors():
    authors = Author.query.all()
    authors_get = [
         {
            "author_name": author.author_name,
            "birth_date": author.birth_date.isoformat(),
            "nationality": author.nationality
         }
         for author in authors
    ]
    return jsonify(authors=authors_get), 200

@routes_bp.route("/authors/<string:author_name>", methods=["GET"])
def get_authors_by_name(author_name):
     author_data = request.get_json()
     birth_date = author_data.get("birth_date", "")
     try:
        author_name = author_data["author_name"]
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        nationality = author_data["nationality"]
        author = Author(
            author_name=author_name,
            birth_date=birth_date,
            nationality=nationality
            )
        db.session.add(author)
        db.session.commit()
        return jsonify(msg="Autor adicionado com sucesso"), 201
     except KeyError as error:
        return jsonify({"error": "Chave faltante: " + str(error)}), 400
     except ValueError:
        return jsonify({"error": "Formato de data inválido. Use AAAA-MM-DD."}), 400