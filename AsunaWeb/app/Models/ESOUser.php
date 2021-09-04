<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ESOUser extends Model
{
    use HasFactory;

    protected $fillable = [
        'family_name'
    ];
}
