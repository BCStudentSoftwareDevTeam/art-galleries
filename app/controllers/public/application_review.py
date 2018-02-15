from . import public
from app.logic.validation import *
from flask import render_template
from app.models.Forms import Forms
from app.models.queries.FormQueries import *


@public.route('/application/review/<int:fid>', methods=["GET", "POST"])
def review(fid):
    form = FormQueries.get(fid)

    return render_template('views/public/application_review.html', form = form)



