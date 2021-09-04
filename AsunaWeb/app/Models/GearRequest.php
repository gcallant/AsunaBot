<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GearRequest extends Model
{
    use HasFactory;

    protected $fillable = [
        'guild_member_id',
        'gear_set_id'
    ];
}
