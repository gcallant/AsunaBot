<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class EventSignup extends Model
{
    use HasFactory;

    protected $primaryKey = 'eventSignupID';

    protected $fillable = [
        'guildMemberID',
        'roleID',
        'eventID',
        'esoCharacterID',
        'noCallNoShow',
        'guildMemberNotes'
    ];

    protected $attributes = [
        'noCallNoShow' => false
    ];
}
