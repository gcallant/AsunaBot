<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearSet extends Model
{
    use HasFactory;

    protected $fillable = [
        'gear_set_name',
        'location_id'
    ];
}
