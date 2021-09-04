<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CharacterRace extends Model
{
    use HasFactory;

    protected $fillable = [
        'race_name'
    ];

    public function esoCharacter(): void
    {
        $this->hasMany(ESOCharacter::class);
    }
}
