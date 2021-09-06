<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class EventSignup extends Model
{
    use HasFactory;

    protected $fillable = [
        'guild_member_id',
        'role_id',
        'event_id',
        'eso_character_id',
        'no_call_no_show',
        'guild_member_notes'
    ];

    protected $attributes = [
        'no_call_no_show' => false
    ];

    public function guildMember() : BelongsTo
    {
        return $this->belongsTo(GuildMember::class);
    }

    public function role() : BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function event() : BelongsTo
    {
        return $this->belongsTo(Event::class);
    }

    public function esoCharacter() : BelongsTo
    {
        return $this->belongsTo(ESOCharacter::class);
    }
}
