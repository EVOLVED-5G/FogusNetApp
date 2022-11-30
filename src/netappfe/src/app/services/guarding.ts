import { CanActivate,CanActivateChild, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import {UserService} from "src/app/services/user.service";
import { Injectable } from '@angular/core';

@Injectable()
export class AuthGuard implements CanActivate,CanActivateChild {
  constructor(private userService: UserService, private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): boolean {
    if(this.userService.isLoggedIn()){
      return true;
    }
    this.router.navigate(['/sign-in']);
    return false;
  }

   canActivateChild(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): boolean {
        if(this.userService.isLoggedIn()){
          return true;
        }
        this.router.navigate(['/sign-in']);
        return false;
      }
    }

