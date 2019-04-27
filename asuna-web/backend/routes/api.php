<?php

use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:api')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('register', 'Auth\RegisterController@register');
Route::post('login', 'Auth\LoginController@login')->name('login');
Route::post('logout', 'Auth\LoginController@logout');

Route::group(['middleware' => 'auth:api'], function() {
    Route::resource('events', 'EventsController');

    Route::resource('users', 'UsersController');
    Route::get('events/{id}/users', 'UsersController@getByEvent');

    Route::get('signups', 'SignupsController@index');
    Route::get('signups/{id}', 'SignupsController@show');
    Route::delete('signups/{id}', 'SignupsController@destroy');
    Route::patch('signups/{id}', 'SignupsController@update');
    Route::post('events/{id}/signups', 'SignupsController@store');
    Route::get('events/{id}/signups', 'SignupsController@getByEvent');
    Route::get('users/{id}/signups', 'SignupsController@getByUser');
});
