<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class CharacterRace extends Model
{
    use HasFactory;

    protected $fillable = [
        'race_name'
    ];

    public function esoCharacter() : HasMany
    {
        return $this->hasMany(ESOCharacter::class);
    }
}
