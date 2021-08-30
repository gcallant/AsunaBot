<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class GuildMember extends Model
{
    use HasFactory;

    protected $primaryKey = 'guildMemberID';
    public $incrementing = false;

    protected $fillable = [
        'guildMemberID',
        'name',
        'discordUserID',
        'discordRoleIDs'
    ];
}
