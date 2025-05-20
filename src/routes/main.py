from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from src.models import ClienteFinalizado

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Página Inicial")

@main_bp.route("/clientes_finalizados/contrato_pronto/<int:cliente_id>")
@login_required
def contrato_pronto(cliente_id):
    return render_template("contrato_pronto.html", cliente_id=cliente_id)