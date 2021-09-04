<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearPiece extends Model
{
    use HasFactory;

    protected $fillable = [
        'gear_piece_name'
    ];
}
