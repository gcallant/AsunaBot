<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

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
}
