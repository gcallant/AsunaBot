<?php

namespace App\Providers;

use Illuminate\Support\Facades\Gate;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     *
     * @var array
     */
    protected $policies = [
        // 'App\Model' => 'App\Policies\ModelPolicy',
    ];

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Gate::define('is-admin', function($user) {
            return config('enums.roles')[$user->role] >= config('enums.roles')['ADMIN'];
        });

        Gate::define('create-event', function($user) {
            return config('enums.roles')[$user->role] >= config('enums.roles')['RAID LEADER'];
        });

        Gate::define('proxy-create-event', function($user) {
            return config('enums.roles')[$user->role] >= config('enums.roles')['ADMIN'];
        });

        Gate::define('edit-event', function($user, $event) {
            $isAdmin = config('enums.roles')[$user->role] >= config('enums.roles')['ADMIN'];
            $isEventCreator = $event->created_by_id == $user->discord_id;
            return $isEventCreator || $isAdmin;
        });
    }
}
