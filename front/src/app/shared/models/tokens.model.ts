export class TokensModel {
  constructor(
    public access_token: string,
    public token_type: string,
    public refresh_token: string
  ) {}
}
