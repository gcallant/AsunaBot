<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class ESOCharacter extends Model
{
    use HasFactory;

    protected $fillable = [
        'eso_user_id',
        'character_name',
        'character_type_id',
        'character_class',
        'character_race_id'
    ];

    protected $attributes = [
        'isCertified' => false
    ];

    public function characterRace() : BelongsToMany
    {
        return $this->belongsToMany(CharacterRace::class);
    }
}
