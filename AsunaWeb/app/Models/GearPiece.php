<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class GearPiece extends Model
{
    use HasFactory;

    protected $fillable = [
        'gear_piece_name'
    ];

    public function gearRequest() : BelongsToMany
    {
        return $this->belongsToMany(GearRequest::class);
    }
}
