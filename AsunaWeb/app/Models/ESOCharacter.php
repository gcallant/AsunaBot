<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ESOCharacter extends Model
{
    use HasFactory;

    protected $primaryKey = 'esoCharacterID';

    protected $fillable = [
        'esoUserID',
        'characterName',
        'characterTypeID',
        'characterClass',
        'characterRaceID'
    ];

    protected $attributes = [
        'isCertified' => false
    ];
}
