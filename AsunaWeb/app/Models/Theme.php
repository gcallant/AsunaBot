<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Theme extends Model
{
    use HasFactory;

    /** Mass assignable attributes
     * @var array
     */
    protected $fillable = [
        'theme_name'
    ];

    public function user() : HasMany
    {
        return $this->hasMany(User::class);
    }
}
