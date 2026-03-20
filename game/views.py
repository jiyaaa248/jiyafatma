from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from learning.models import UserProfile
import json


@login_required
def game_hub(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    games = [
        {
            'name': 'Firewall Guardian',
            'slug': 'firewall',
            'description': 'Defend against corrupted C++ code packets. Click valid syntax, ignore the bugs. How long can your shield last?',
            'xp_reward': 'Up to 200 XP',
            'difficulty': 'Medium',
            'difficulty_color': '#f59e0b',
            'emoji': '🛡️',
            'tag': 'Syntax',
            'bg': 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
        },
        {
            'name': 'Code Memory Matrix',
            'slug': 'memory',
            'description': 'Memorize C++ code cards and match them before the timer runs out. Train your muscle memory for real syntax.',
            'xp_reward': 'Up to 150 XP',
            'difficulty': 'Easy',
            'difficulty_color': '#10b981',
            'emoji': '🧠',
            'tag': 'Memory',
            'bg': 'linear-gradient(135deg, #064e3b 0%, #065f46 100%)',
        },
        {
            'name': 'C++ Type Speed',
            'slug': 'typespeed',
            'description': 'Type real C++ code as fast as you can. Accuracy and speed both matter. Race the clock and earn XP per correct character!',
            'xp_reward': 'Up to 300 XP',
            'difficulty': 'Hard',
            'difficulty_color': '#ef4444',
            'emoji': '⚡',
            'tag': 'Speed',
            'bg': 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)',
        },
    ]
    return render(request, 'game/game_hub.html', {
        'games': games,
        'profile': profile,
        'user_xp': profile.xp,
        'user_level': profile.level,
    })


@login_required
def firewall_game(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'game/firewall.html', {
        'profile': profile,
        'csrf_token': request.META.get('CSRF_COOKIE', ''),
    })


@login_required
def memory_game(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'game/memory.html', {'profile': profile})


@login_required
def typespeed_game(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'game/typespeed.html', {'profile': profile})


@login_required
def update_xp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score = int(data.get('score', 0))
            game = data.get('game', 'unknown')

            # Cap XP per game session to prevent abuse
            caps = {'firewall': 200, 'memory': 150, 'typespeed': 300}
            max_xp = caps.get(game, 200)
            score = min(score, max_xp)
            score = max(score, 0)

            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.xp += score
            profile.level = (profile.xp // 100) + 1
            profile.save()

            return JsonResponse({
                'status': 'success',
                'xp_earned': score,
                'total_xp': profile.xp,
                'level': profile.level,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)
