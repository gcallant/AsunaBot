<?php

namespace App\Http\Controllers\Auth;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Foundation\Auth\AuthenticatesUsers;

class LoginController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | Login Controller
    |--------------------------------------------------------------------------
    |
    | This controller handles authenticating users for the application and
    | redirecting them to your home screen. The controller uses a trait
    | to conveniently provide its functionality to your applications.
    |
    */

    use AuthenticatesUsers;

    /**
     * Where to redirect users after login.
     *
     * @var string
     */
    protected $redirectTo = '/home';

    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('guest')->except('logout');
    }

    /**
    * Overwrite default login verification to only require password.
    *
    * @param  \Illuminate\Http\Request  $request
    * @return void
    *
    * @throws \Illuminate\Validation\ValidationException
    */
    protected function validateLogin(Request $request)
    {
        $this->validate($request, [
            'authcode' => 'required|string',
            'password' => 'required|string',
        ]);
    }

    /**
     * Overwrite the default credentials to only require the password.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    protected function credentials(Request $request)
    {
        return $request->only('authcode', 'password');
    }

}
