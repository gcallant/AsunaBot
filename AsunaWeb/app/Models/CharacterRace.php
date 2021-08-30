<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CharacterRace extends Model
{
    use HasFactory;

    protected $primaryKey = 'characterRaceID';

    protected $fillable = [
        'raceName'
    ];
}
