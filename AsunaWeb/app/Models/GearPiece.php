<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearPiece extends Model
{
    use HasFactory;

    protected $primaryKey = 'gearPieceID';

    protected $fillable = [
        'gearPieceName'
    ];
}