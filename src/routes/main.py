@main_bp.route("/clientes_finalizados/contrato_pronto/<int:cliente_id>")
@login_required
def contrato_pronto(cliente_id):
    return render_template("contrato_pronto.html", cliente_id=cliente_id)