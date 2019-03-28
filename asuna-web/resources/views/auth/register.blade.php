@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">{{ __('Register') }}</div>

                <div class="card-body">
                    <form method="POST" action="{{ route('register') }}">
                        @csrf

                        <div class="form-group row">
                            <label for="eso_name" class="col-md-4 col-form-label text-md-right">{{ __('ESO Name') }}</label>

                            <div class="col-md-6">
                                <input id="eso_name" type="text" class="form-control{{ $errors->has('eso_name') ? ' is-invalid' : '' }}" name="eso_name" value="{{ old('eso_name') }}" autofocus>

                                @if ($errors->has('eso_name'))
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $errors->first('eso_name') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group row">
                            <label for="discord_id" class="col-md-4 col-form-label text-md-right">{{ __('Discord ID') }}</label>

                            <div class="col-md-6">
                                <input id="discord_id" type="text" class="form-control{{ $errors->has('discord_id') ? ' is-invalid' : '' }}" name="discord_id" value="{{ old('discord_id') }}" required>

                                @if ($errors->has('discord_id'))
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $errors->first('discord_id') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group row">
                            <label for="authcode" class="col-md-4 col-form-label text-md-right">{{ __('Authcode') }}</label>

                            <div class="col-md-6">
                                <input id="authcode" type="text" class="form-control{{ $errors->has('authcode') ? ' is-invalid' : '' }}" name="authcode" required>

                                @if ($errors->has('authcode'))
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $errors->first('authcode') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group row mb-0">
                            <div class="col-md-6 offset-md-4">
                                <button type="submit" class="btn btn-primary">
                                    {{ __('Register') }}
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
