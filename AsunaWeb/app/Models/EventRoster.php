<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class EventRoster extends Model
{
    use HasFactory;

    protected $fillable = [
        'max_tanks',
        'max_heals',
        'max_ranged_dps',
        'max_melee_dps'
    ];
}
