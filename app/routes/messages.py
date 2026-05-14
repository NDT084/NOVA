from flask import Blueprint, request, jsonify, session
from app.models.message import save_message
from app import pusher_client

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/message/send', methods=['POST'])
def send():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Non autorisé'}), 401

    data = request.get_json()
    group_id = data.get('group_id')
    content = data.get('content')
    ghost = data.get('ghost', False)

    if not group_id or not content:
        return jsonify({'status': 'error', 'message': 'Données manquantes'}), 400

    save_message(group_id, session['user_id'], content, is_ghost=ghost)

    # 1. Déclencher la mise à jour du chat en temps réel (Votre code existant)
    pusher_client.trigger(
        f'group-{group_id}',
        'new-message',
        {
            'username': session['username'],
            'content': content,
            'ghost': ghost
        }
    )

    # 2. DÉCLENCHER LA NOTIFICATION VISUELLE GLOBALE (Ajout dynamique)
    try:
        pusher_client.trigger(
            'nova-channel', 
            'new-message-event', 
            {
                'title': f"📩 Message de {session['username']}",
                'message': content if not ghost else "👻 Un message fantôme a été partagé."
            }
        )
    except Exception as e:
        print(f"Erreur Pusher passée en silence : {e}")

    return jsonify({
        'status': 'ok',
        'username': session['username'],
        'ghost': ghost
    })
