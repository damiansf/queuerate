from flask import Blueprint, request
from app.models import Category, Link
from app.services.APIResponseBuilder import APIResponseBuilder
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.tasks import tasks
import json

category_controller = Blueprint("category_controller", __name__)


@category_controller.route('/demo')
def demo():
    link = Link(url='localhost', user_id="aaabbbcccddd", link_title="test", link_description="test desc")
    db.session.add(link)
    db.session.commit()
    print("Starting process")
    tasks.process_link(link)
    print("Ending process")
    return "Initialized"


@category_controller.route('/', methods=['GET'])
def get_all_categories():
    """
    Returns a JSON response of all categories in the system
    Does not include associated keywords
    """
    try:
        categories = Category.query.all()
        return APIResponseBuilder.success({
         "categories": categories
        })
    except SQLAlchemyError as e:
        return APIResponseBuilder.error(f"Issue running query: {e}")
    except Exception as e:
        return APIResponseBuilder.error(f"Error encountered: {e}")


@category_controller.route('/<category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """
    Returns a JSON response of a single category with id of category_id
    Includes all single keywords associated with that category

    :param  category_id: ID of the specific category to be found
    :return: JSON response
    """
    try:
        category = Category.query.get(category_id)
        # Return category if successful, return fail if category not found matching that id
        if category:
            return APIResponseBuilder.success({"category": category})
        else:
            return APIResponseBuilder.failure({
                "invalid_id": f"Unable to find category with id {category_id}"
            })
    except SQLAlchemyError as e:
        return APIResponseBuilder.error(f"Issue running query: {e}")
    except Exception as e:
        return APIResponseBuilder.error(f"Error encountered: {e}")


@category_controller.route('/', methods=['POST'])
def create_new_category():
    """
    Create a new category with the passed information

    :return: JSON of new category if successful, error response if not
    """
    try:
        data = request.form.to_dict()
        # We'll never want a category to be archived by default so we can ignore the is_archived param
        # and just go with the default
        category = Category(
            user_id=data["user_id"],
            category_name=data["category_name"],
        )
        db.session.add(category)
        db.session.commit()
        return APIResponseBuilder.success({
            "category": category
        })
    except SQLAlchemyError as e:
        return APIResponseBuilder.error(f"Issue running query: {e}")
    except Exception as e:
        return APIResponseBuilder.error(f"Error encountered: {e}")


@category_controller.route('/<category_id>', methods=['PATCH'])
def update_category_by_id(category_id):
    """
    Update a category represented by category_id.
    Attributes that can change:
    is_archived: Archive status
    category_name: category can be renamed

    :param category_id: ID of the category to be updated
    :return: JSON response with the updated category entity
    """
    try:
        data = request.form.to_dict()
        category = Category.query.get(category_id)
        if category:
            category.category_name = data['category_name']
            # category.is_archived = data['is_archived'] or False TODO: find way to convert JSON true -> python Bool
            db.session.commit()
            return APIResponseBuilder.success({
                "category": category
            })
        else:
            return APIResponseBuilder.failure({
                "invalid_id": f"Unable to find category with ID of {category_id}"
            })
    except SQLAlchemyError as e:
        return APIResponseBuilder.error(f"Issue running query: {e}")
    except Exception as e:
        return APIResponseBuilder.error(f"Error encountered: {e}")


@category_controller.route('/<category_id>/links', methods=["GET"])
def get_all_links_by_category(category_id):
    """
    Returns a JSON response of all links by category
    Does not include associated categories

    :param :category_id
    """
    # TODO: validate category ID
    try:
        category = Category.query.get(category_id)
        return APIResponseBuilder.success({
            "links": category.links
        })
    except SQLAlchemyError as e:
        return APIResponseBuilder.error(f"Issue running query: {e}")
    except Exception as e:
        return APIResponseBuilder.error(f"Error encountered: {e}")

