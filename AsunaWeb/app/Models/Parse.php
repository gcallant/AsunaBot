<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Parse extends Model
{
    use HasFactory;

    protected $fillable = [
        'dps',
        'parse_file_path'
    ];

    public function esoCharacter() : HasMany
    {
        return $this->hasMany(ESOCharacter::class);
    }
}
